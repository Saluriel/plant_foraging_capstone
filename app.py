import os
from flask import Flask, render_template, request, flash, redirect, session, g, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json


from forms import UserAddForm, LoginForm, EditUserForm
from models import db, connect_db, User, PlantPin, Serializer

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///foraging_db'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
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

    If form not valid, re-present form.

    If the there is already a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                location=form.location.data,
            )
            db.session.commit()

        except IntegrityError as err:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Shows the login form and handles user login."""

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
    """Shows form for and handles editing the user's information"""
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

@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """Renders the user's profile"""
    if g.user:
        user = User.query.get_or_404(user_id)
        return render_template('/users/profile.html', user=user)

@app.route('/')
def homepage():
    """Renders the homepage for logged in users and a sign up message for not logged in users"""
    if g.user:
        return render_template('homepage.html')

    else:
        return render_template('home-anon.html')


# Map related routes
@app.route("/map", methods=["GET", "POST"])
def show_map_handle_pins():
    """Renders a map"""

    if g.user:
        plant_pins = PlantPin.query.all()
       
        return render_template('/maps/view_map.html', plant_pins=plant_pins)

    else:
        return render_template('home-anon.html')

@app.route('/handle_map', methods=["POST"])
def handle_map():
    """Handles adding a pin to the database, returns json"""
    
    if g.user:
        if request.method == "POST":
            received = request.get_json()
            print("RECEIVED DATA", received)
            if received["plant"] == '':
                return error('Plant must be named')
            else:
                now = datetime.now()

                user_id = g.user.id
                date = now.strftime("%m/%d/%Y, %H:%M:%S")
                plant = received["plant"]
                plantPin = PlantPin(user_id = user_id, date = date, plant=plant, latitude=received["latitude"], longitude=received["longitude"])
                db.session.add(plantPin)
                db.session.commit()
                result = {'latitude': received["latitude"], 'longitude':received["longitude"], 'plant': received["plant"]}
            return jsonify(result)
    else:
        return redirect('/')

@app.route('/view_pins')
def view_pin_list():
    """View a list of all the pins made"""
    if g.user:
        plant_pins = PlantPin.query.all()
        return render_template('/maps/pin_list.html', plant_pins=plant_pins)

    else:
        return redirect('/')

@app.route('/api/pins')
def load_map():
    """Api page for the pins so that JS can access them"""
    if g.user:
        pins = PlantPin.query.all()
        
        return json.dumps(Serializer.serialize_list(pins))
    
    else:
        return redirect('/')

@app.route("/pins/<int:pin_id>")
def load_single_pin(pin_id):
    """Loads a single pin on the map"""
    if g.user:
        pin = PlantPin.query.get_or_404(pin_id)
        return render_template('/maps/single_pin.html', pin=pin)

@app.route("/pins/delete/<int:pin_id>", methods=["GET", "POST"])
def edit_pin(pin_id):
    """Renders and handles deleting a pin"""
    if g.user:
        pin = PlantPin.query.get_or_404(pin_id)
        db.session.delete(pin)
        db.session.commit()
        return redirect('/')
        
    else:
        return redirect('/')
        
    