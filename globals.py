from surveys import surveys
from helpers import survey_size

# initialize global variables
responses = []
survey_key = 'dummy'
active_survey = surveys[survey_key]
(num_questions, columns) = survey_size(active_survey)
allowing_text = []
completed_surveys = [survey_key]