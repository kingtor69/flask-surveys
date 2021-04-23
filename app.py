# app.py written entirely by Tor Kingdon

from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
from helpers import survey_size
# import globals

app = Flask(__name__)
app.config['SECRET_KEY'] = "big-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def set_up_session():
	
	# return render_template('home.html')

@app.route('/home')
def build_home_html():
	if session.get('completed_surveys'):
		if len(surveys) == len(session['completed_surveys']):
			flash("THANK YOU. You have completed all of our surveys.", "info")
			flash("Please check back later to see if there are any new surveys", "info")

	return render_template('home.html', surveys = surveys)


	
@app.route('/question/<url_pt2>', methods=['POST', 'GET'])
def display_next_question(url_pt2):
	"""process previous page and move on to next question"""

	# first things first: load responses and completed surveys into temp variables
	#? might be unnecessary, but I couldn't make pushing to a list in the session work
	# lst = dic.get('list') if type(dic.get('list')) == list else []
	temp_responses = session.get('responses') if type(session.get('response')) == list else []
	temp_completed_surveys = session.get('completed_surveys') if type(session.get('completed_surveys')) == list else []

	# is there an active survey key in the session?
	if not session.get('active_survey_key'):
		flash("line 77 - nothing in the session under active survey", "troubleshooting")
		flash("a survey was never chosen", "error")
		flash("please choose a survey", "info")
		return redirect('/')

	# load survey object from surveys using session's survey key
	#? also might be unnecessary, but it seemed to me the survey dictionary didn't save properly in the session, so it was better to use a reference to it
	active_survey = surveys[session['active_survey_key']]
	(num_questions, columns) = survey_size(active_survey)

	# if the URL is non-numeric, it was manually entered and must go back to the start
	if not url_pt2.isnumeric():
		flash("interger expected where there was none in url", "error")
		# TODO: is it possible to figure out where we should be from the session and redirect there?
		flash("insuffienct data to continue", "error")
		flash("please choose a survey", "info")
		return redirect('/')

	# convert the URL to an integer
	question = int(url_pt2)
	# determine the question we need next
	where_are_we = len(temp_responses)
	# is this the first question after choosing the survey?
	if where_are_we == 0 and question == 0:
		chosen_key = request.form['key']
		session['active_survey_key'] = chosen_key
		active_survey = surveys[chosen_key]
		(num_questions, columns) = survey_size(active_survey)
		try:
			# if surveys.values().get(active_survey):
			return render_template('question.html', question_id = question, question_num = question + 1, survey = active_survey, key = chosen_key, columns = columns)
		except:
			flash ("I wrote this when it was line 97. I don't expect to see it again unless I break something else :/", "troubleshooting")
			flash ("we can't find a chosen survey", "error")
			flash ("please try again", "info")
			return redirect('/')
	
	# are we on a valid question URL (i.e. the # matches the next one we need)
	if where_are_we == question:
		try:
			return render_template('question.html', question_id = question, question_num = question + 1, survey = active_survey, key = session['active_survey_key'], columns = columns)
		except:
			flash("bad url", "error")
			flash("line 113", "troubleshooting")
			flash("seemed good, but template failed to render", "troubleshooting")
			flash("insuffienct data to continue", "error")
			flash("please choose a survey", "info")
			return redirect('/')

	# redirect to home page if a user manually navigates to a question page wihtout selecting a survey:
	if session.get('active_survey') == "dummy":
		flash('this was line 120 when I last saw it', 'troubleshooting')
		flash("a survey was never chosen", "error")
		flash("please choose a survey", "info")
		return redirect('/')

	# we're only at this point if a question has just been answered
	if not request.form.get('choice'):
		flash("no choice was made", "error")
		flash("please select an answer", "info")
		return render_template(f'question.html', question_id = question - 1, question_num = question, survey = session['active_survey_key'], columns = columns)

	# enter answer (and text) into session['responses']
	# k, right now, the "choice" is being entered twice but not sticking around
	if request.form.get('elaboration'):
		temp_responses.append([request.form['choice'], request.form['elaboration']])
		if session.get('allowing_text'):
			session['allowing_text'].append(question - 1)
		# else:
		# 	session['allowing_text'].append = [question - 1]
	else:
		try:
			temp_responses.append(request.form['choice'])
			session['responses'].append(request.form['choice'])
		except:
			flash("bad data on form", "error")
			flash("please try this question again", "info")
			session['responses'] = temp_responses
			return redirect(f'/question/{where_are_we}')
	

	# if user just answered the last question of the survey:
	if question == len(active_survey.questions):
		temp_completed_surveys.append(session['active_survey_key'])
		session['completed_surveys'] = temp_completed_surveys
		session['responses'] = temp_responses
		return redirect('/response')

	# user has at least one more question to answer
	session['responses'] = temp_responses
	return render_template('question.html', question_id = question, question_num = question +1, survey = active_survey, key = session['active_survey_key'], columns = columns)

@app.route('/response')
def survey_done():
	""" survey is complete, load thank you page with summary of user's answers"""

	# load survey object from surveys using session's survey key
	active_survey = surveys[session['active_survey_key']]
	(num_questions, columns) = survey_size(active_survey)

	return render_template('response.html', survey = active_survey, num_questions = num_questions, columns = columns)

@app.route('/reset')
def reset_and_restart():
	"""clears flask session and goes back to beginning"""
	session.clear()
	return redirect('/')