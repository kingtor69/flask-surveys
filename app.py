# app.py written entirely by Tor Kingdon

from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys
from helpers import survey_size
import globals

app = Flask(__name__)
app.config['SECRET_KEY'] = "big-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

@app.route('/')
def landing_page():
	"""reset global variables
	if there are not availble surveys left for this user, send a message to that effect
	display either message or avaiables surveys for user to choose from"""
	globals.responses = []
	globals.types = []

	if len(surveys) == len(globals.completed_surveys):
		flash("THANK YOU. You have completed all of our surveys.", "info")
		flash("Please check back later to see if there are any new surveys", "info")
	
	return render_template('home.html', surveys = surveys, completed_surveys = globals.completed_surveys)

# if we're GETting a request, it's not from our forms
@app.route('/question/<url_pt2>', methods=['GET'])
def this_is_not_my_beautiful_page(url_pt2):
	"""if we are receiving a GET request on this page, it did not come from one of our forms and needs to be dealt with accordingly"""
	if url_pt2.isnumeric():
		where_are_we = len(globals.responses)
		question = int(url_pt2)
		if question == where_are_we:
			try:
				flash(globals.responses_flash)
				return render_template('question.html', question_id = question, question_num = question +1, survey = globals.active_survey, key = globals.survey_key, columns = globals.columns)
			except: 
				flash("insuffienct data to continue", "error")
				flash("please choose a survey", "info")
				return redirect('/')

	flash("bad url entered", "error")
	flash("please choose a survey", "info")
	return redirect('/')
	
@app.route('/question/<int:question>', methods=['POST'])
def display_next_question(question):
	"""process previous page and move on to next question"""
	where_are_we = len(globals.responses)

	globals.survey_key = request.form['key']
	# determine the number of the page we should be on

	# if this is the first question of the selected survey
	if where_are_we == 0 and question == 0:
		globals.survey_key = request.form['key']
		globals.active_survey = surveys[globals.survey_key]
		(globals.num_questions, globals.columns) = survey_size(globals.active_survey)
		return render_template('question.html', question_id = question, question_num = question + 1, survey = globals.active_survey, key = globals.survey_key, columns = globals.columns)

	# redirect to home page if a user manually navigates to a question page wihtout selecting a survey:
	if globals.survey_key == "dummy":
		flash("a survey was never chosen", "error")
		flash("please choose a survey", "info")
		return redirect('/')

	# we're only at this point if a question has just been answered
	if not request.form['choice']:
		flash("no choice was made", "error")
		flash("please select an answer", "info")
		return render_template('question.html', question_id = question - 1, question_num = question, survey = globals.active_survey, key = globals.survey_key, columns = globals.columns)

	# was there a text field in the question?
	if not request.form.get('elaborate'):
		globals.responses.append(request.form['choice'])
	elif request.form.get('eleborate') and request.form.get('choice'):
		globals.responses.append([request.form['choice'], request.form['elaboration']])
	else:
		flash("bad data on form", "error")
		flash("please try this question again", "info")
		return redirect(f'/question/{where_are_we}')

	# if user just answered the last question of the survey:
	if len(globals.responses) == globals.num_questions:
		# globals.survey_done = True
		globals.completed_surveys.append(globals.survey_key)
		for i in range(globals.num_questions):
			globals.types.append(type(globals.responses[i]))
		return redirect('/response')

	# user has at least one more question to answer
	return render_template('question.html', question_id = question, question_num = question +1, survey = globals.active_survey, key = globals.survey_key, columns = globals.columns)

@app.route('/response')
def survey_done():
	try:
		return render_template('response.html', survey = globals.active_survey, responses = globals.responses, num_questions = globals.num_questions, columns = globals.columns, types = globals.types)
	except:
		flash("this survey wasn't completed properly", "error")
		flash("please try again", "info")
		return redirect('/')

@app.route('/reset')
def reset_and_restart():
	"""resets all parameters and starts over"""
	globals.responses = []
	globals.survey_key = 'dummy'
	globals.active_survey = surveys[globals.survey_key]
	(globals.num_questions, globals.columns) = survey_size(globals.active_survey)
	globals.types = []
	globals.completed_surveys = [globals.survey_key]
	return redirect('/')