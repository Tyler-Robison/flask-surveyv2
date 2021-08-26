from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


responses = []


@app.route('/')
def home_page():
    """Displays survey title and instructions
    Contains button to start the survey
    """

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    responses.clear()

    return render_template('home.html', title=title, instructions=instructions)


@app.route('/questions/<q_number>')
def show_question(q_number):
    """
    Directs you to the correct page based on number questions answered
    If user tries to alter URL will re-direct to correct URL 
    If user tries to re-enter survey after completion will re-direct to thank you page
    """

    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')

    question = satisfaction_survey.questions[len(responses)].question

    q_number = int(q_number)
    if q_number != len(responses):
        flash('Please answer questions in correct order')
        return redirect(f'/questions/{len(responses)}')

    if len(responses) == 0:
        return render_template('firstq.html', question=question)
    elif len(responses) == 1:
        return render_template('secondq.html', question=question)
    elif len(responses) == 2:
        return render_template('thirdq.html', question=question)
    elif len(responses) == 3:
        return render_template('fourthq.html', question=question)


@app.route('/answers', methods=["POST"])
def answer():
    """
    Adds user answer to response list
    Then redirects to correct URL based on # questions answered
    """

    for ele in request.form.values():
        responses.append(ele)

    if len(responses) == 1:
        return redirect('/questions/1')
    elif len(responses) == 2:
        return redirect('/questions/2')
    elif len(responses) == 3:
        return redirect('/questions/3')
    elif len(responses) == len(satisfaction_survey.questions):
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    """
    Thank you page displayed upon survey completion
    Redirects user to correct question if they try to access early
    """
    if len(responses) != len(satisfaction_survey.questions):
        return redirect(f'/questions/{len(responses)}')

    return render_template('thanks.html', responses=responses)
