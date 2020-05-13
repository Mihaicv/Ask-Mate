from flask import Flask, render_template, request, redirect, url_for
import data_manager
from datetime import datetime

app = Flask(__name__)


@app.route("/", methods=['GET', 'POST'])
def main():
    sort_by = ''
    direction = ''
    if request.method == "POST":
        sort_by = request.form.get('sort')
        direction = request.form.get('direction')
        data = data_manager.sort_csv(sort_by, direction)
    else:
        data = data_manager.get_questions()

    return render_template('all_questions.html', questions=data, sort_by=sort_by, direction=direction)


@app.route("/add_new_question", methods=["GET", "POST"])
def add_question():

    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        view_number = 0
        vote_number = 0
        title = request.form['title'],
        message = request.form["message"],
        image = request.form['image']
        data_manager.add_question(submission_time, view_number, vote_number, title, message, image)
        return redirect('/')
    return render_template('add_new_question.html')


@app.route('/question/<id>', methods=['GET', 'POST'])
def show_question(id):
    answers = data_manager.get_answer()
    view = data_manager.find_question(id)[0]
    view_no = view.get('view_number', '')
    data_manager.view_question(id, view_no)
    answer_by_question_id = data_manager.find_answer_by_question_id(id)
    question = data_manager.find_question(id)[0]
    comment_id_question = data_manager.get_comments_by_question_id(id)
    tabel_comment = data_manager.get_tabel_comment()
    return render_template('question.html', question=question, answers=answers,
                           answer_by_question_id=answer_by_question_id, comment_id_question=comment_id_question,
                           tabel_comment=tabel_comment)


@app.route('/question/<question_id>/edit', methods=['GET', 'POST'])
def edit_question(question_id):
    question = data_manager.find_question(question_id)[0]
    if request.method == 'POST':
        title = request.form.get('title')
        message = request.form.get("message")
        image = request.form.get('image')
        data_manager.edit_question(question_id, title, message, image)
        return redirect('/')
    return render_template('edit.html', question=question, id=question_id)


@app.route('/question/<question_id>/delete', methods=['GET', 'POST'])
def delete_question(question_id):
    data_manager.delete_question(question_id)
    return redirect('/')


@app.route('/question/<question_id>/new_answer', methods=['GET', 'POST'])
def new_answer(question_id):
    now = datetime.now()
    question = data_manager.find_question(question_id)
    if request.method == 'POST':
        submission_time = now.strftime("%m/%d/%Y %H:%M:%S")
        vote_number = 0
        question_id = question_id
        message = request.form.get("message")
        image = request.form.get('image')
        data_manager.new_answer(submission_time, vote_number, question_id, message, image)
        return redirect('/question/' + str(question_id))
    return render_template('new_answer.html', id=question_id)


@app.route('/answer/<answer_id>/delete', methods=['GET', 'POST'])
def delete_answer(answer_id):
    data_manager.delete_answer_by_id(answer_id)
    return redirect(request.referrer)


@app.route("/question/<question_id>/vote_up")
def Q_vote_up(question_id):
    data_manager.vote_up_question(question_id)
    return redirect(request.referrer)


@app.route("/question/<question_id>/vote_down")
def Q_vote_down(question_id):
    data_manager.vote_down_question(question_id)
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote_up")
def A_vote_up(answer_id):
    data_manager.vote_up_answer(answer_id)
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote_down")
def A_vote_down(answer_id):
    data_manager.vote_down_answer(answer_id)
    return redirect(request.referrer)


@app.route('/question/<question_id>/new-comment', methods=['GET', 'POST'])
def add_question_comment(question_id):
    questions = data_manager.find_question(question_id)
    now = datetime.now()
    if request.method == 'POST':
        question_id = question_id
        message = request.form.get('message')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_comment_question(question_id, message, submission_time)
        return redirect('/question/' + str(question_id))
    return render_template('add_question_comment.html', questions=questions)


@app.route('/comments/<comment_id>/delete', methods=['GET', 'POST'])
def delete_qu_comment(comment_id):
    data_manager.delete_coment_by_id_qu(comment_id)
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True,
            port=5001)
