from datetime import datetime

from flask import Flask, render_template, request, make_response
import jwt

from app.database.action import Action
from app.database.movie import Movie
from app.database.user import User


app = Flask(__name__)
sort_field = 'title'


def make_homepage(request=None):
    """
    Makes the homepage based on the request received
    Checks if there is an authentication token and if there is one,
    returns the user preferences and user object
    """
    user = None
    user_preferences = None
    if 'auth_token' in request.cookies:
        auth_token = request.cookies.get('auth_token')
        user_info = jwt.decode(auth_token, 'secret', algorithms=['HS256'])
        user = User.select_by_user_id(user_info['user_id'])
        if user:
            user_preferences = Action.select_user_preferences(user['id'])

    movies_data = Movie.select_all()

    dict_values = {'user': user, 'movies_data': movies_data, 'user_preferences': user_preferences}

    return dict_values


@app.route("/movies/all")
@app.route("/")
def index():
    """
    Endpoint that gets all movies from Database
    """
    dict_values = make_homepage(request)

    return render_template("index.html", movies_data=dict_values['movies_data'], user=dict_values['user'],
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'])


@app.route("/sort_by", methods=['GET'])
def sort_movies():
    """
    Endpoint that changes the sort field
    """
    dict_values = make_homepage(request)

    query_parameters = request.args
    sort_field = query_parameters.get('field')

    return render_template("index.html", movies_data=dict_values['movies_data'], user=dict_values['user'],
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'])


@app.route("/movies/<int:user_id>", methods=['GET'])
def movies_by_user(user_id):
    """
    Endpoint that gets the movies based on user id from Database
    """
    dict_values = make_homepage(request)
    dict_values['movies_data'] = Movie.select_by_userid(user_id)

    return render_template("index.html", movies_data=dict_values['movies_data'], user=dict_values['user'],
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'])


@app.route("/movies/create", methods=['POST'])
def create_movie():
    """
    Endpoint that creates a new movie in the Database
    """
    if not Movie.check_movie_exists(request.form['title']):
        return render_template('error.html', error_message="Movie already exists!"), 201

    auth_token = request.cookies.get('auth_token')
    user_info = jwt.decode(auth_token, 'secret', algorithms=['HS256'])

    movie = Movie(request.form['title'], request.form['description'],
                  user_info['user_id'], datetime.now(), datetime.now())
    movie.insert()

    dict_values = make_homepage(request)

    return render_template("index.html", movies_data=dict_values['movies_data'], user=dict_values['user'],
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'])


@app.route("/users/create", methods=['POST'])
def create_user():
    """
    Endpoint that creates a new user in the Database, creates a new authentication token, saves it as cookie
    and returns them to browser
    """
    if not User.check_email_exists(request.form['email']):
        return render_template('error.html', error_message="Email already exists!"), 201

    user = User(request.form['first_name'], request.form['last_name'],
                request.form['email'], request.form['password'],
                datetime.now(), datetime.now())

    user.insert()

    encoded_jwt = jwt.encode({'user_id': user.id, 'first_name': user.first_name, 'last_name': user.last_name},
                             'secret', algorithm='HS256').decode("utf-8")

    dict_values = make_homepage(request)

    resp = make_response(render_template("index.html", movies_data=dict_values['movies_data'], user=user,
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'], token=encoded_jwt))
    resp.set_cookie('auth_token', encoded_jwt)

    return resp


@app.route("/users/auth", methods=['POST'])
def authenticate_user():
    """
    Endpoint that authenticates user from Database
    """
    user = User.authenticate(request.form['email'], request.form['password'])
    if user is None:
        return render_template('error.html', error_message="Wrong email or password!"), 201

    movies_data = Movie.select_all()
    user_preferences = Action.select_user_preferences(user['id'])

    encoded_jwt = jwt.encode({'user_id': user['id'], 'first_name': user['first_name'], 'last_name': user['last_name']},
                             'secret', algorithm='HS256').decode("utf-8")

    resp = make_response(render_template("index.html", movies_data=movies_data, user=user, sort_field=sort_field,
                                         user_preferences=user_preferences, token=encoded_jwt))
    resp.set_cookie('auth_token', encoded_jwt)

    return resp


@app.route("/actions/like/<int:movie_id>", methods=['GET'])
def create_action_like(movie_id):
    """
    Endpoint that creates a positive (like) action in the Database
    """
    auth_token = request.cookies.get('auth_token')
    user_info = jwt.decode(auth_token, 'secret', algorithms=['HS256'])

    action = Action(True, movie_id, user_info['user_id'], datetime.now(), datetime.now())
    action.insert()

    dict_values = make_homepage(request)

    return render_template("index.html", movies_data=dict_values['movies_data'], user=dict_values['user'],
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'])


@app.route("/actions/dislike/<int:movie_id>", methods=['GET'])
def create_action_dislike(movie_id):
    """
    Endpoint that creates a negative (dislike) action in the Database
    """
    auth_token = request.cookies.get('auth_token')
    user_info = jwt.decode(auth_token, 'secret', algorithms=['HS256'])

    action = Action(False, movie_id, user_info['user_id'], datetime.now(), datetime.now())
    action.insert()

    dict_values = make_homepage(request)

    return render_template("index.html", movies_data=dict_values['movies_data'], user=dict_values['user'],
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'])


@app.route("/actions/remove/<int:action_id>", methods=['GET'])
def remove_action(action_id):
    """
    Endpoint that deletes an action from the Database
    """
    Action.delete(action_id)

    dict_values = make_homepage(request)

    return render_template("index.html", movies_data=dict_values['movies_data'], user=dict_values['user'],
                           sort_field=sort_field, user_preferences=dict_values['user_preferences'])


@app.route("/add_movie", methods=['GET'])
def add_movie_form():
    """
    Endpoint that redirects to movie form
    """
    return render_template('add_movie.html')


@app.route("/sign_up", methods=['GET'])
def sign_up_form():
    """
    Endpoint that redirects to sign up form
    """
    return render_template('sign_up.html')


@app.route("/login", methods=['GET'])
def login_form():
    """
    Endpoint that redirects to login form
    """
    return render_template('login.html')


