from flask import Flask, redirect, url_for, render_template, session, abort, request
from forms import RegisterForm, LoginForm, SearchForm, AddFriendForm, DeleteFriendForm
import bcrypt
import config
from database import Database

app = Flask(__name__)
app.secret_key = config.app_secret_key


@app.route('/')
@app.route('/index')
def index():
    if 'loggedin' in session:
        return redirect(url_for("my_profile"))
    return render_template('index.html')


@app.route('/login', methods=['get', 'post'])
def login():
    form = LoginForm()
    password_check = None
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data.encode('utf-8')
        db_connection = Database()
        user_db = db_connection.get_password_hash(username)
        if user_db:
            password_hash = user_db['password'].encode('utf-8')
            if bcrypt.checkpw(password, password_hash):
                session['loggedin'] = True
                session['username'] = username
                return redirect(url_for("index"))
            else:
                password_check = False
        else:
            password_check = False
    return render_template('login.html', form=form, password_check=password_check)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/registration', methods=['get', 'post'])
def registration():
    if 'loggedin' not in session:
        form = RegisterForm()
        if form.validate_on_submit():
            username = form.username.data
            firstname = form.firstname.data
            lastname = form.lastname.data
            email = form.email.data
            gender = form.gender.data
            city = form.city.data
            age = form.age.data
            interest = form.interest.data
            password = bcrypt.hashpw(form.password.data.encode('utf8'), bcrypt.gensalt(14)).decode('utf-8')
            db_connection = Database()
            if db_connection.check_user_exist(username, email):
                return render_template('registration.html', form=form, user_exist=True)
            else:
                db_connection.add_user(username, firstname, lastname, email, gender, city, age, interest, password)
                return render_template('registration_successful.html')
        return render_template('registration.html', form=form)
    else:
        return redirect(url_for("index"))


@app.route('/user/<username>', methods=['get', 'post'])
def user(username):
    if 'loggedin' in session:
        if session['username'] != username:
            db_connection = Database()

            user_info_values = db_connection.get_user(username)
            if user_info_values:
                user_info_values = list(user_info_values.values())
                user_info_attributes = ['Логин', 'Имя', 'Фамилия', 'Возраст', 'Город', 'Интересы']
                user_info = dict(zip(user_info_attributes, user_info_values))

                form_add = AddFriendForm()
                form_delete = DeleteFriendForm()
                friend_status = db_connection.friend_status(session['username'], username)
                if friend_status:
                    init_friend_request = friend_status['user_one']
                    friend_status = friend_status['status']
                else:
                    init_friend_request = None

                friends_list_db = db_connection.get_friend_list(username)
                friend_list = []
                if friends_list_db:
                    for friend in friends_list_db:
                        friend_list.append(list(friend.values())[0])

                if request.method == 'POST':
                    form_method = list(request.form.keys())[1]
                    if form_method == 'form_delete':
                        db_connection.friend_delete(session['username'], username)
                    if form_method == 'form_add':
                        db_connection.friend_request(session['username'], username)
                    return redirect(url_for("user", username=username))

                return render_template('profile.html', user_info=user_info, form_add=form_add, form_delete=form_delete, \
                                       friend_status=friend_status, init_friend_request=init_friend_request, \
                                       friend_list=friend_list)
            else:
                abort(404)
        else:
            return redirect(url_for("my_profile"))
    else:
        return redirect(url_for("index"))


@app.route('/search', methods=['get', 'post'])
def search():
    form = SearchForm()
    if form.validate_on_submit():
        db_connection = Database()
        search = form.search.data
        db_request = db_connection.search_user(search)
        find_dict = dict()
        if db_request:
            for result in db_request:
                find_dict[result['username']] = {'firstname': result['firstname'], 'lastname': result['lastname'], 'city': result['city']}
            return render_template('search.html', form=form, find_dict=find_dict)
    return render_template('search.html', form=form)


@app.route('/my-profile', methods=['get', 'post'])
def my_profile():
    if 'loggedin' in session:
        form = AddFriendForm()
        username = session['username']
        db_connection = Database()

        user_info_values = list(db_connection.get_user(username).values())
        user_info_attributes = ['Логин', 'Имя', 'Фамилия', 'Возраст', 'Город', 'Интересы']
        user_info = dict(zip(user_info_attributes, user_info_values))

        db_friend_requests = db_connection.get_friend_requests(username)
        friend_requests = []
        for friend_request in db_friend_requests:
            friend_requests.append(friend_request['user_one'])
        if request.method == 'POST':
            form_method = list(request.form.values())[1]
            friend_username = list(request.form.keys())[1]
            if form_method == 'Принять заявку':
                db_connection.approved_friend_request(friend_username, username)
            if form_method == 'Отказаться':
                db_connection.skip_friend_request(friend_username, username)
            return redirect(url_for("my_profile"))

        friends_list_db = db_connection.get_friend_list(username)
        friend_list = []
        if friends_list_db:
            for friend in friends_list_db:
                friend_list.append(list(friend.values())[0])
        return render_template('my-profile.html', form=form, user_info=user_info, \
                               friend_requests=friend_requests, friend_list=friend_list)
    else:
        return redirect(url_for("index"))


if __name__ == '__main__':
    app.run()
