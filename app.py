from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "chickensarecool123456"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

survey_completed = False
change_number = None

@app.route('/')
def home_page():
    """
    Displays survey title and instructions
    Contains button to start the survey
    """

    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    session['responses'] = []

    return render_template('home.html', title=title, instructions=instructions)


@app.route('/survey/<q_number>', methods=['POST', 'GET'])
def display_question(q_number):

    q_number = int(q_number)

    if len(session['responses']) == 4:
        return redirect('/thanks')

    if len(session['responses']) != q_number:
        return redirect(f'/survey/{len(session["responses"])}')

    question = satisfaction_survey.questions[q_number].question

    if len(session['responses']) == 0:
        return render_template('firstq.html', question=question)
    elif len(session['responses']) == 1:
        return render_template('secondq.html', question=question)
    elif len(session['responses']) == 2:
        return render_template('thirdq.html', question=question)
    elif len(session['responses']) == 3:
        return render_template('fourthq.html', question=question)


@app.route('/answers', methods=["POST"])
def answer():
    """
    Adds user answer to response list
    Then redirects to correct URL based on # questions answered
    """
    if survey_completed == True:
        for ele in request.form.values():
            responses = session['responses']
            responses[change_number] = ele
            session['responses'] = responses
        return redirect('/thanks')   


    for ele in request.form.values():
        responses = session['responses']
        responses.append(ele)
        session['responses'] = responses

    if len(session['responses']) == 1:
        return redirect('/survey/1')
    elif len(session['responses']) == 2:
        return redirect('/survey/2')
    elif len(session['responses']) == 3:
        return redirect('/survey/3')
    elif len(session['responses']) == len(satisfaction_survey.questions):
        return redirect('/thanks')


@app.route('/thanks')
def thanks():
    """
    Thank you page displayed upon survey completion
    Redirects user to correct question if they try to access early
    """
    if len(session['responses']) != len(satisfaction_survey.questions):
        return redirect(f'/survey/{len(session["responses"])}')

    ans_dct = {}
   
    for count, ele in enumerate(satisfaction_survey.questions):
        ans_dct[ele.question] = session['responses'][count]  

    return render_template('thanks.html', dct=ans_dct)

@app.route('/change/<q_number>')
def change_answer(q_number):
    """
    Allows changing a particular answer from thanks page
    """
    q_number = int(q_number)

    global survey_completed 
    survey_completed = True

    global change_number
    change_number = q_number

    question = satisfaction_survey.questions[q_number].question

    if q_number == 0:
        return render_template('firstq.html', question=question)
    elif q_number == 1:
        return render_template('secondq.html', question=question)
    elif q_number == 2:
        return render_template('thirdq.html', question=question)
    elif q_number == 3:
        return render_template('fourthq.html', question=question)

