# Flask Surveys
## The Story
 0. software checks if there is are any completed surveys in the session
 0. software redirects route / to:
 1. /home (home.html) - user chooses a survey from a list of available surveys 
   - software does not display any completed surveys
 1. software saves chosen survey to session
 2. /question/# (question.html) user is directed to first question in the survey
 3. when user answers that question, they keep going
 4. software enters into session:
   - whether there was a text box in the question
   - append answer into a list 
   - (and text box in an array within the responses array)
 5. user is directed to next question
 6. repeat steps question > next question steps until last question
 7. on last question, redirect to a finished page
 8. mark the survey as complete in session data
 9. thank the user and display their answers
 10. redirect them back to home page
