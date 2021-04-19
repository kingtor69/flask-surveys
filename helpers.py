def survey_size(survey):
	"""returns a tuple of the numbers of columns and rows this survey will occupy

	columns default 2, but if any of the questions allow for a text field response, this function changes that to 3

	rows is the number of questions in the survey

	>>> satisfaction_survey = Survey(
	    "Customer Satisfaction Survey",
	    "Please fill out a survey about your experience with us.",
	    [
	        Question("Have you shopped here before?"),
	        Question("Did someone else shop with you today?"),
	        Question("On average, how much do you spend a month on frisbees?",
	                 ["Less than $10,000", "$10,000 or more"]),
	        Question("Are you likely to shop here again?"),
	    ])

	>>> personality_quiz = Survey(
	    "Rithm Personality Test",
	    "Learn more about yourself with our personality quiz!",
	    [
	        Question("Do you ever dream about code?"),
	        Question("Do you ever have nightmares about code?"),
	        Question("Which is the worst function name, and why?",
	                 ["do_stuff()", "run_me()", "wtf()"],
	                 allow_text=True),
	    ])

	>>> column_count(satisfacton_survey)
	(4, 2)

	>>> column_count(personality_quiz)
	(3, 3)

    """

	columns = 2
	num_questions = len(survey.questions)
	any_text_allowed = False
	for i in range(num_questions):
		if survey.questions[i].allow_text:
			any_text_allowed = True
	if any_text_allowed:
		columns = 3

	return (num_questions, columns)