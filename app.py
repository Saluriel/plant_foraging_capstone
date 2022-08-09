import os
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError

from forms import UserAddForm, LoginForm, EditUserForm
from models import db, connect_db, User, Plant, PlantPin

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///foraging_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")
toolbar = DebugToolbarExtension(app)

connect_db(app)

# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None

def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.
    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                location=form.location.data or User.location.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/sgnup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid username or password.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You've been logged out successfully!")
    return redirect("/login")

# General User Routes:
@app.route('/edit/<user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    """Handles editing the user's information"""
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    else:
        form = EditUserForm()
        form.username.default = g.user.username
        form.email.default=g.user.email
        form.location.default=g.user.location
    
    if form.validate_on_submit():
        user = User.authenticate(g.user.username,
                                 form.password.data)
        if user == False:
            flash("Wrong password, please enter your current password", "danger")
            return redirect('/users/profile')

        else:
            try:
                g.user.username = form.username.data
                g.user.email = form.email.data
                g.user.location = form.location.data
                db.session.add(g.user)
                db.session.commit()
                return redirect(f'/edit/{user_id}')

            except IntegrityError:
                flash("Username already taken", 'danger')
                return redirect(f'/edit/{user_id}')
    else: 
        form.process()      
        return render_template('/users/edit.html', form=form)
        


@app.route('/')
def homepage():
    if g.user:
        return render_template('homepage.html')

    else:
        return render_template('home-anon.html')
    