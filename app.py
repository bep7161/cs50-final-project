import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
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


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """ Show the portfolio of projects """

    # Get username of current logged in user
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]

    # Get the users projects 
    projects = db.execute("SELECT * FROM projects WHERE user_id = ?", session["user_id"])

    # When the user clicks the button for one of their projects
    if request.method == "POST":
        project_id = request.form["project_id"]
        url = "/edit_project/" + str(project_id)
        return redirect(url)

    # Return the index template with the projects variable
    else:
        return render_template("index.html", user=user, projects=projects)


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


@app.route("/register", methods=["GET", "POST"])
def register():
    """ Allow the user to register a new account """

    # Clear any possible session
    session.clear()

    # User reaches route via POST (i.e. they submitted the form)
    if request.method == "POST":
        # Check username is filled in
        if not request.form.get("username"):
            return apology("Must provide username", 403)
        
        # Check password was filled in
        elif not request.form.get("password"):
            return apology("Must provide password", 403)
        
        #Check confirmation was filled in
        elif not request.form.get("confirmation"):
            return apology("Must confirm password", 403)
        
        #Check password and confirmation match
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Password and confirmation did not match", 403)
        
        # Query the database to see if the username already exists
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username"))
        
        # If the username exists tell the user
        if len(rows) == 1:
            return apology("Username already exists", 403)
        
        # All checks are complete add new user to the db
        db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", request.form.get("username"),
                   generate_password_hash(request.form.get("password"), method="scrypt", salt_length=16))
        
        # Redirect user to login page to use new credentials to login
        return redirect("/login")
    
    # User reached route via GET (i.e. clicked the button or entered the link)
    else:
        return render_template("register.html")


@app.route("/new_project", methods=["GET", "POST"])
@login_required
def new_project():
    """ Allow user to create a new project """
    # Get username of current logged in user
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]

    # User reached route via POST (i.e. clicked the submit button)
    if request.method == "POST":
        # Check name field is populated
        if not request.form.get("name"):
            return apology("Must provide project name", 403, user)
        
        # Check descrisption is populated
        elif not request.form.get("description"):
            return apology("Must provide a project description", 403, user)
        
        # Check start date is populated
        elif not request.form.get("start_date"):
            return apology("Must provide the start date", 403, user)
        
        #Check end date is populated
        elif not request.form.get("end_date"):
            return apology("Must provide the end date", 403, user)

        # All checks compelte, update projects table with new project
        db.execute("INSERT INTO projects (user_id, name, description, start_date, end_date) VALUES(?, ?, ?, ?, ?)",
                   session["user_id"], request.form.get("name"), request.form.get("description"), 
                   request.form.get("start_date"), request.form.get("end_date"))
        
        # Redirect user to the project page and allow them to add tasks
        return redirect("/")
    
    # User reached route via GET (i.e. clicked the link)
    else:
        return render_template("new_project.html", user=user)
    

@app.route("/delete_project", methods=["GET", "POST"])
@login_required
def delete_project():
    """ Allow user to delete any of their projects """
    # Get username of current logged in user
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]

    # Get the users projects 
    projects = db.execute("SELECT * FROM projects WHERE user_id = ?", session["user_id"])

    # User reached route via POST (i.e. clicked the delete button)
    if request.method == "POST":
        # Get project id from the button
        id = request.form.get("project_id")

        # Delete project and tasks from databases
        db.execute("DELETE FROM tasks WHERE project_id = ?", id)
        db.execute("DELETE FROM projects WHERE id = ?", id)        

        # Redirect back to the delete proejcts page
        return redirect("/delete_project")

    # User reached route via GET (i.e. clicked the link)
    else:
        return render_template("delete_project.html", user=user, projects=projects)


@app.route("/edit_project/<project_id>", methods=["GET", "POST"])
@login_required
def edit_project(project_id):
    """ Allow users to edit their project and tasks """
    # Get username of current logged in user
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]

    # Get the users project
    projects = db.execute("SELECT * FROM projects WHERE id = ?", project_id)

    # Get the tasks for that user's project
    tasks = db.execute("SELECT * FROM tasks WHERE project_id = ? ORDER BY end_date", project_id)

    # User clicks one of the two buttons on the page
    if request.method == "POST":
    
        # If the user clicked the Update Project button
        if "project_update" in request.form:
            # Update projects database with fields
            db.execute("UPDATE projects SET name = ?, description = ?, start_date = ?, end_date = ?, percent_complete = ?, status = ?, phase = ? WHERE id = ?",
                       request.form.get("name"), request.form.get("description"), request.form.get("start_date"), request.form.get("end_date"),
                       request.form.get("percent_complete"), request.form.get("status"), request.form.get("phase"), project_id)
            
            url = "/edit_project/" + project_id
            return redirect(url)
        
        # If the user clicked the Add Task button
        elif "add_task" in request.form:
            # Insert new task into database
            db.execute("INSERT INTO tasks (user_id, project_id, name, description, assigned_to, state, start_date, end_date) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                       session["user_id"], project_id, request.form.get("name"), request.form.get("description"), request.form.get("assigned_to"),
                       request.form.get("state"), request.form.get("start_date"), request.form.get("end_date"))

            url = "/edit_project/" + project_id
            return redirect(url)

        # If the user clicked the Update button
        elif "task_update" in request.form:
            # Update task table with information for this specific
            db.execute("UPDATE tasks SET name = ?, description = ?, assigned_to = ?, state = ?, start_date = ?, end_date = ? WHERE id = ?",
                       request.form.get("name"), request.form.get("description"), request.form.get("assigned_to"), request.form.get("state"),
                       request.form.get("start_date"), request.form.get("end_date"), request.form.get("task_update"))
            
            url = "/edit_project/" + project_id
            return redirect(url)

    # User reached route via GET (i.e. clicked the link)       
    else:
        return render_template("edit_project.html", project_id=project_id, user=user, projects=projects, tasks=tasks)


@app.route("/openai")
@login_required
def openai():
    # Get username of current logged in user
    user = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]

    return apology("Under Construction!", 400, user)