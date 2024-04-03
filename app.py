import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Create helpers file and import the helper functions
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of assinged cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50's library to use sqlite for the database
db = SQL("sqlite:///projects.db")


@app.after_request
def after_request(response):
    """ Ensure responses aren't cached """
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    return apology("Not ready yet", 400)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ Login the user """

    # Forget any user_id or sessions running
    session.clear()

    # User reaches route via POST (i.e. clicked the Log In button)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("Must provide password", 403)
        
        # Query the database for the username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))
        
        # Ensure username exists and passwork is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)

        # Remeber which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")
    
    # User reach via GET (i.e. clicking link or redirect)
    else:
        return render_template("login.html")
    

@app.route("/logout")
def logout():
    """ Log the user out """

    # Forget any sessions running
    session.clear()

    # Redirect user to login
    return redirect("/")