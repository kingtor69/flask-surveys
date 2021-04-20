# app.py written entirely by Tor Kingdon

from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
from helpers import survey_size

app = Flask(__name__)
app.config['SECRET_KEY'] = "big-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def set_up_session():
	"""set up Flask session to store user's progress separately from anyone else's"""

	# if user has saved info in a session, keep it. if not, start with default values to be replaced later

	if not session.get('active_survey'):
		session['active_survey_key'] = 'dummy'
	if not session.get('completed_surveys'):
		session['completed_surveys'] = ['dummy']
	if not session.get('responses'):
		session['responses'] = []
	return redirect('/home')
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
		
	# if the URL is non-numeric, it was manually entered and must go back to the start
	if not url_pt2.isnumeric():
		flash("bad url", "error")
		flash("insuffienct data to continue", "error")
		flash("please choose a survey", "info")
		return redirect('/')

	# convert the URL to an integer
	question = int(url_pt2)
	# determine the question we need next
	where_are_we = len(session.get('responses'))
	# is this the first question after choosing the survey?
	if where_are_we == 0 and question == 0:
		# chosen_key = request.form['key']
		if session.get('active_survey_key'):
			chosen_key = session['active_survey_key']
		else:
			flash ("we can't find a chosen survey", "error")
			flash ("please try again", "info")
			return redirect('/')
		session['active_survey_key'] = chosen_key
		active_survey = surveys[chosen_key]
		(num_questions, columns) = survey_size(active_survey)
		try:
			# if surveys.values().get(active_survey):
			return render_template('question.html', question_id = question, question_num = question + 1, survey = active_survey, key = session['active_survey_key'], columns = columns)
		except:
			flash ("we can't find a chosen survey", "error")
			flash ("please try again", "info")
			return redirect('/')
	
	print('*****0000000000000000*******')
	print(session.get('responses'))
	print('#######000000000000000#####')
	# are we on a valid question URL (i.e. the # matches the next one we need)
	if where_are_we == question:
		try:
			return render_template('question.html', question_id = question, question_num = question + 1, survey = active_survey, key = session['active_survey_key'], columns = columns)
		except:
			flash("bad url", "error")
			flash("insuffienct data to continue", "error")
			flash("please choose a survey", "info")
			return redirect('/')


	# get the size of the chosen survey:
	active_survey = surveys[session['active_survey_key']]
	(num_questions, columns) = survey_size(active_survey)

	# redirect to home page if a user manually navigates to a question page wihtout selecting a survey:
	if session.get('survey_key') == "dummy":
		flash('is this where it failed?', 'troubleshooting')
		# YES, but when did the key get turned back into dummy?
		flash("a survey was never chosen", "error")
		flash("please choose a survey", "info")
		return redirect('/')

	# we're only at this point if a question has just been answered
	if not request.form.get('choice'):
		flash("no choice was made", "error")
		flash("please select an answer", "info")
		return render_template('question.html', question_id = question, question_num = question + 1, survey = active_survey, key = session['active_survey_key'], columns = columns)

	# enter answer (and text) into session['responses']

	if request.form.get('elaboration'):
		session['responses'][question - 1] = ([request.form['choice'], request.form['elaboration']])
		if session.get('allowing_text'):
			session['allowing_text'][question - 1] = (question - 1)
		else:
			session['allowing_text'][question - 1] = None
	else:
		try:
			session['responses'][question - 1] = (request.form['choice'])
		except:
			flash("bad data on form", "error")
			flash("please try this question again", "info")
			return redirect(f'/question/{where_are_we}')

	# if user just answered the last question of the survey:
	if question == len(active_survey.questions):
		session['completed_surveys'].append(session['active_survey_key'])
		print('******11111111111111******')
		print(session.get('responses'))
		print('#######111111111111111111#########')
		return redirect('/response')

	# user has at least one more question to answer
	return render_template('question.html', question_id = question, question_num = question +1, survey = active_survey, key = session['active_survey_key'], columns = columns)

@app.route('/response')
def survey_done():
	print('*****222222222222222******')
	print(session.get('responses'))
	print('########2222222222222222222#########')
	active_survey = surveys[session['active_survey_key']]
	(num_questions, columns) = survey_size(active_survey)
	print('******3333333333333333333*********')
	print(session.get('responses'))
	print('#######333333333333############')
	try:
		return render_template('response.html', survey = active_survey, num_questions = num_questions, columns = columns)
	except:
		return render_template('debug.html')
		flash("something went wonky in this survey", "error")
		flash("it's probably my bad", "info")
		flash("please try again or pick another one", "info")
		flash("just don't hate me", "info")
		return redirect('/')

@app.route('/reset')
def reset_and_restart():
	"""resets all parameters and starts over"""
	globals.responses = []
	globals.survey_key = 'dummy'
	globals.active_survey = surveys[globals.survey_key]
	(globals.num_questions, globals.columns) = survey_size(globals.active_survey)
	globals.allowing_text = []
	globals.completed_surveys = [globals.survey_key]
	return redirect('/')