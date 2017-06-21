"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route('/register', methods=["GET"])
def register_form():
    """Takes user's info and sends to registration form."""

    email = request.args.get("email")
    password = request.args.get("password")

    return render_template("register_form.html", email=email, password=password)


@app.route('/register', methods=["POST"])
def register_process():
    """Receives user's info and redirects to the homepage. """

    email = request.form.get("email")
    password = request.form.get("password")

    if (User.query.filter_by(email=email).first()) == None:
        # check if they exist already. If not, then register them.
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
    #else:
        # put up a flash message or an alert that tells them they exist and to login

    return redirect("/")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)


    
    app.run(port=5000, host='0.0.0.0')
