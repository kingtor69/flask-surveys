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
def phone_home():
	# 0. software redirects route / to:
	return redirect('/home')

@app.route('/home')
def build_home_html():
	completed_surveys = session.get('completed_surveys', [])
	session['completed_surveys'] = completed_surveys
	
	return render_template('home.html', surveys = surveys)

@app.route('/question/0', methods = ['POST', 'GET'])
def question_zero:
	return render_template('question.html')

# @app.route('/question/<int:question>', methods=['POST', 'GET'])
# def display_next_question(question):
# 	if not session.get('survey_key'):
# 		try:
# 			session['survey_key'] = request.form['survey'])
# 		except:
# 			flash('please choose a survey', 'info')
# 			return redirect('/home')
	
# 	survey_key = ('survey_key')

# 	responses = session.get('responses', [])
# 	responses.append(request.form['choice'])
# 	session['responses'] = responses

# 	if question == len(surveys[survey_key])
# 		completed_surveys = session.get('completed_surveys', [])
# 		completed_surveys.append(survey_key)
# 		session['completed_surveys'] = completed_surveys
# 		return redirect('/response')
	
# 	return render_template('question.html, (num_questions, columns) = helpers.survey_size(survey_key)')

	# -- question/0
	# 1. software saves chosen survey to session
	# 2. /question/# (question.html) user is directed to first question in the survey
	# 3. when user answers that question, they keep going


	# -- question/>0
	# 4. software enters into session:
	# - whether there was a text box in the question
	# - append answer into a list 
	# - (and text box in an array within the responses array)
	# 5. user is directed to next question
	# 6. repeat steps question > next question steps until last question

	# question = len(survey.questions)
	# 7. on last question, redirect to a finished page
	return render_template('question.html', survey_key = survey_key, question_id = question, question_num = question + 1)


@app.route('/response')
def survey_done():
	""" survey is complete, load thank you page with summary of user's answers"""

	# 8. mark the survey as complete in session data
	# 9. thank the user and display their answers
	# 10. redirect them back to home page
	return render_template('response.html', survey = active_survey, num_questions = num_questions, columns = columns)

@app.route('/reset')
def reset_and_restart():
	"""clears flask session and goes back to beginning"""
	session.clear()
	return redirect('/')