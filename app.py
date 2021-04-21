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
	"""set up Flask session to store user's progress separately from anyone else's"""

	# initialize temp variables with startup values
	temp_active_survey = 'dummy'
	temp_responses = []
	temp_completed_surveys = []

	# if user has a saved survey in progress, remplate those values into temp variables
	# if not, initiatlize session object with startup values

	if session.get('active_survey'):
		temp_active_survey = session['active_survey']
	else:
		session['active_survey_key'] = 'dummy'
	if session.get('completed_surveys'):
		temp_completed_surveys = session['completed_surveys']
	else:
		session['completed_surveys'] = temp_completed_surveys
	if session.get('responses'):
		temp_responses = session['responses']
	else:
		session['responses'] = temp_responses

	# if the survey is in progress, head on over to the next question
	if session.get('active_survey') and not session.get('active_survey') == 'dummy':
		next_question = len(temp_responses)
		(num_questions, columns) = survey_size(surveys['active_survey'])
		return render_template('question.html', survey = session['active_survey'], num_questions = num_questions, columns = columns)

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
	

	print('*****-1-1-1-1-1-1*******')
	print(session.get('responses'))
	for response in request.form:
		print(response)
		print(request.form[response])
	print('#######-1-1-1-1-1-1#####')
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
	print('********where-and-which***********')
	print(where_are_we)
	print(question)
	print('###########where-and-which###########')
	if where_are_we == 0 and question == 0:
		print("*****and we're in########")
		chosen_key = request.form['key']
		session['active_survey_key'] = chosen_key
		active_survey = surveys[chosen_key]
		(num_questions, columns) = survey_size(active_survey)
		try:
			# if surveys.values().get(active_survey):
			return render_template('question.html', question_id = question, question_num = question + 1, survey = active_survey, key = session['active_survey_key'], columns = columns)
		except:
			flash ("I think this is our first except and the problem is on the stupid template", "troubleshooting")
			flash ("we can't find a chosen survey", "error")
			flash ("please try again", "info")
			return redirect('/')
	

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
	if session.get('active_survey') == "dummy":
		flash('this was line 103 when I wrote it?', 'troubleshooting')
		# YES, but when did the key get turned back into dummy?
		flash("a survey was never chosen", "error")
		flash("please choose a survey", "info")
		return redirect('/')

	# we're only at this point if a question has just been answered
	if not request.form.get('choice'):
		flash("no choice was made", "error")
		flash("please select an answer", "info")
		return render_template(f'question.html', question_id = question - 1, question_num = question, survey = session['active_survey_key'], columns = columns)

	# enter answer (and text) into responses key in session cookie
	if request.form.get('elaboration'):
		print ('********AAAAAARRRRRRRAAAAAAYYYYYYYY*********')
		print ('this is where we should be appending to responses')
		print ('#######AAAAAARRRRRRRAAAAAAYYYYYYYY##########')
		temp_responses.append([request.form['choice'], request.form['elaboration']])
		print ('********AAAAAARRRRRRRAAAAAAYYYYYYYY*********')
		print ('and it should be done')
		print (session.get('responses'))
		print ('the before array is')
		print (session.get('responses'))
		print ('#######AAAAAARRRRRRRAAAAAAYYYYYYYY##########')

		
		if session.get('allowing_text'):
			session['allowing_text'].append(question - 1)
		# else:
		# 	session['allowing_text'].append = [question - 1]
	else:
		print ('********SSSSSTTTTTRRRRRRRIIIIINNNNNGGGGGGG*********')
		print ('this is where we should be appending to responses')
		print ('the before array is')
		print (session.get('responses'))
		print ('#######SSSSSTTTTTRRRRRRRIIIIINNNNNGGGGGGG##########')
		try:
			temp_responses.append(request.form['choice'])
			print ('********SSSSSTTTTTRRRRRRRIIIIINNNNNGGGGGGG*********')
			print ('and it should be done')
			print (session.get('responses'))
			print ('#######SSSSSTTTTTRRRRRRRIIIIINNNNNGGGGGGG##########')
		except:
			flash("bad data on form", "error")
			flash("please try this question again", "info")
			return redirect(f'/question/{where_are_we}')

	# if user just answered the last question of the survey:
	if question == len(active_survey.questions):
		temp_completed_surveys.append(session['active_survey_key'])
		print('******11111111111111******')
		print(session.get('responses'))
		print('#######111111111111111111#########')
		return redirect('/response')

	# user has at least one more question to answer
	return render_template('question.html', question_id = question, question_num = question +1, survey = active_survey, key = session['active_survey_key'], columns = columns)

@app.route('/response')
def survey_done():
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
	if session.get('responses'):
		session['responses'] = []
	if session.get('survey_key'):
		session['survey_key'] = 'dummy'
	if session.get('allowing_text'):
		session['allowing_text'] = []
	if session.get('completed_surveys'):
		session['completed_surveys'] = []
	return redirect('/')