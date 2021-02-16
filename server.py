from flask import Flask, render_template, request, redirect, url_for, flash, session
import data_manager
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret'


@app.route('/')
def list_last_questions():
    data = data_manager.get_last_questions()
    return render_template('all_questions.html', questions=data)


@app.route("/list", methods=['GET', 'POST'])
def list_all_questions():
    sort_by = ''
    direction = ''
    if request.method == "POST":
        sort_by = request.form.get('sort')
        direction = request.form.get('direction')
        data = data_manager.sort_questions(sort_by, direction)
    else:
        data = data_manager.get_questions()

    return render_template('all_questions.html', questions=data, sort_by=sort_by, direction=direction, searching=True)


@app.route("/add_new_question", methods=["GET", "POST"])
def add_question():
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        view_number = 0
        vote_number = 0
        title = request.form['title'],
        message = request.form["message"],
        image = request.form['image']
        id_user = session['user_id']
        data_manager.add_question(submission_time, view_number, vote_number, title, message, image, id_user)
        data_manager.update_users_questions(session['user_id'])
        return redirect('/')
    return render_template('add_new_question.html')


@app.route('/question/<id>', methods=['GET', 'POST'])
def show_question(id):
    tags = data_manager.get_all_tags()
    question_t = data_manager.all_question_tag()
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
                           tabel_comment=tabel_comment, tags=tags, question_t=question_t)


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
    question = data_manager.find_question(question_id)
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        vote_number = 0
        question_id = question_id
        message = request.form.get("message")
        image = request.form.get('image')
        id_user = session['user_id']
        data_manager.new_answer(submission_time, vote_number, question_id, message, image, id_user)
        data_manager.update_users_answers(session['user_id'])
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

    if request.method == 'POST':
        question_id = question_id
        message = request.form.get('message')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        id_user = session['user_id']
        data_manager.add_comment_question(question_id, message, submission_time, id_user)
        data_manager.update_users_comments(session['user_id'])
        return redirect('/question/' + str(question_id))
    return render_template('add_question_comment.html', questions=questions)


@app.route('/comments/<comment_id>/delete', methods=['GET', 'POST'])
def delete_qu_comment(comment_id):
    data_manager.delete_coment_by_id_qu(comment_id)
    return redirect(request.referrer)


@app.route('/search')
def search():
    phrase = request.args.get('search_text')
    if phrase == '':
        flash('Insert letters')
        return redirect(request.referrer)
    else:
        search_text = data_manager.search(phrase)
        answers = data_manager.get_answer()
    return render_template('search.html', search_text=search_text, phrase=phrase, answers=answers)


@app.route('/answer/<answer_id>/edit', methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer = data_manager.find_answer(answer_id)[0]
    if request.method == 'POST':
        message = request.form.get('message')
        image = request.form.get('image')
        data_manager.edit_answer(answer_id, message, image)
        return redirect('/question/' + str(answer['question_id']))
    return render_template('edit_answer.html', answer=answer)


@app.route('/comment/<comment_id>/edit', methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager.find_comment(comment_id)[0]
    if request.method == 'POST':
        if comment['edited_count'] is not None:
            edit_comm = comment['edited_count'] + 1
        else:
            edit_comm = 1
        message = request.form.get('message')
        data_manager.edit_comment(comment_id, message, edit_comm)
        return redirect('/question/' + str(comment['question_id']))
    return render_template('edit_comment.html', comment=comment)


@app.route('/answer/<answer_id>/new-comment', methods=['GET', 'POST'])
def add_comment_answer(answer_id):
    answer = data_manager.find_answer(answer_id)[0]
    if request.method == 'POST':
        answer_id = answer_id
        message = request.form.get('new_comment')
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_manager.add_answer_comment(answer_id, message, submission_time)
        return redirect('/question/' + str(answer['question_id']))
    return render_template('add_comment_answer.html', answer=answer)


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_tags(question_id):
    tags = data_manager.get_all_tags()
    question = data_manager.find_question(question_id)[0]
    if request.method == 'POST':
        name = request.form.get('tag')
        try:
            data_manager.add_tag(name)
            tag_id = data_manager.get_tag_id(name)
            data_manager.add_tag_in_question_tag(question_id, tag_id['id'])
            return redirect('/question/' + str(question_id))
        except:
            flash("Tag exist")
            return redirect('/question/' + str(question_id))

    return render_template('add_tags.html', question=question, tags=tags)


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager.delete_tag(question_id, tag_id)
    return redirect('/question/' + str(question_id))


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        submission_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        email = request.form.get('email')
        password = request.form.get('password')
        if password == request.form.get('confirm_password'):
            user_registered = data_manager.register_user(submission_time, email, password)
        else:
            flash('Password incorect')
            return redirect('/registration')
        if user_registered == False:
            flash('This email exist')
            return redirect('/registration')
        return redirect(url_for("login"))
    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'email' in session:
        return redirect('/')
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = data_manager.email_exist(email)
        if data_manager.check_login_user(email, password):
            session['email'] = email
            session['user_id'] = user['id_user']
            return redirect('/')
        else:
            flash('Invalid email or password')
            return redirect('/login')
    return render_template('login.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('email')
    return redirect(url_for('login'))


@app.route('/users', methods=['GET', 'POST'])
def users():
    list_users = data_manager.get_users_register()
    return render_template('users.html', list_users=list_users)


@app.route('/user/<user_id>')
def user_page(user_id):
    user = data_manager.find_id_user(user_id)
    question = data_manager.find_questions_id_user(user_id)
    answer = data_manager.find_answer_id_user(user_id)
    comment = data_manager.find_comment_id_user(user_id)
    return render_template('user_page.html', user=user, question=question, answer=answer, comment=comment)


@app.route('/tags', methods=['GET', 'POST'])
def tag_count():
    page_tag = data_manager.tags_count()

    return render_template('tag_count.html', page_tag=page_tag)


if __name__ == "__main__":
    app.run(debug=True,
            port=5005)
