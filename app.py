# app.py written entirely by Tor Kingdon

from flask import Flask, request, render_template, redirect, flash, session, make_response
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, survey_size

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
	session.clear()
	session['completed_surveys'] = completed_surveys
	return render_template('home.html', surveys = surveys)


@app.route('/question/<int:question>', methods=['POST', 'GET'])
def display_next_question(question):
	"""if there is no form data, redirect to previous page
	otherwise, process form data and ask next question"""
	if not session.get('survey_key'):
		try:
			session['survey_key'] = request.form['key']
		except:
			flash('no survey choice registered', 'error')
			flash('please choose a survey', 'info')
			return redirect('/home')

	if not request.form.get('choice'):
		flash('no response was registered for this question', 'error')
		flash('please try again', 'info')
		return redirect(f'/question/{question}')

	survey_key = session['survey_key']
	survey = surveys[survey_key]
	# we're ready to proceed if this was question 0
	(num_questions, columns) = survey_size(survey)
	has_text = (session.get('has_text', []))
	has_text.append(False)
	responses = session.get('responses', [])

	if question > 0:
		# does question have a text box?
		if survey.questions[question].allow_text:
			has_text[question] = True
			elaboration = request.form.get('elaboration', '<left blank>')
			response = [request.form['choice'], elaboration]
		else:
			response = request.form['choice']

		responses.append(response)

	# are we done?
	if question == num_questions:
		completed_surveys = session.get('completed_surveys', [])
		completed_surveys.append(survey_key)
		session['completed_surveys'] = completed_surveys
		return redirect('/response')
	
	session['has_text'] = has_text
	session['responses'] = reseponses
	session['survey_key'] = survey_key
	
	return render_template('question.html', question_id = question, question_num = question + 1, survey = survey, columns = columns)

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



@app.route('/response')
def survey_done():
	""" survey is complete, load thank you page with summary of user's answers"""
	key = session['survey_key']
	completed_surveys = session.get('completed_surveys', [])
	completed_surveys.append(key)
	survey = surveys[key]
	(num_questions, columns) = survey_size(survey)
	session['completed_surveys'] = completed_surveys
	
	return render_template('response.html', survey = survey, num_questions = num_questions, columns = columns)

@app.route('/reset')
def reset_and_restart():
	"""clears flask session and goes back to beginning"""
	session.clear()
	return redirect('/')