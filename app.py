from flask import Flask, render_template, redirect, request, url_for, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = 'random_string12112'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


# responses = []


@app.route('/')
def display_home_page():
	'''display initial information about the survey and button to start the survey'''
	title = satisfaction_survey.title
	instructions = satisfaction_survey.instructions

	return render_template('start.html', survey_title = title, survey_instructions = instructions)


@app.route('/start', methods=['POST'])
def start_survey():
	'''initialize the session to save the users responses and start the survey'''
	session['responses'] = []
	return redirect('/questions/0')


@app.route('/questions/<q_id>', methods=["GET", "POST"])
def display_questions(q_id):
	'''shows each question from the survey to the user with the options for answering the question and a button to submit their answer'''
	question_id = int(q_id)
	if len(session['responses']) == len(satisfaction_survey.questions):
			return redirect('/thanks')
	else:
		if question_id >= len(satisfaction_survey.questions) or question_id != len(session['responses']): 
			flash("That is not a valid question id. Please answer the question below first")
			new_id = len(session['responses'])
			return redirect(f'/questions/{new_id}')
		else: 
			survey_question = satisfaction_survey.questions[question_id].question
			choices = satisfaction_survey.questions[question_id].choices
			return render_template('question.html', question_id=question_id, survey_question=survey_question, choices=choices)


@app.route('/answer', methods=["GET", "POST"])
def collect_answers():
	'''gets answers from the user for each question in the survey'''
	answer = request.form["choices"]

	responses = session['responses']
	responses.append(answer)
	session['responses'] = responses

	q_id = request.form["q_id"]
	new_id = int(q_id) + 1
	if new_id >= len(satisfaction_survey.questions):
		return redirect('/thanks')
	else:
		return redirect(f'/questions/{new_id}')


@app.route('/thanks')
def display_thanks():
	'''show list of questions with user generated answers to thank user for participating in the survey'''
	lst_of_qs = []
	for i in range(len(satisfaction_survey.questions)):
		lst_of_qs.append(satisfaction_survey.questions[i].question)
	
	response_dict = zip(lst_of_qs, session['responses'])

	return render_template('thanks.html', response_dict = response_dict)