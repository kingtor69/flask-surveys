from surveys import surveys
from helpers import survey_size

def show_surveys():
	for survey in surveys:
		(num_questions, columns) = survey_size(surveys[survey])
		print(f'key: {survey}')
		print(f'title: {surveys[survey].title}')
		print(f'instructions: {surveys[survey].instructions}')
		for i in range(num_questions):
			print(f'question{i}: {surveys[survey].questions[i].question}')
			print(f'text?: {surveys[survey].questions[i].allow_text}')
		print()

	return