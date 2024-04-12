# cs50-final-project - PM Tools
#### Video Demo: <URL HERE>
#### Description:
PM Tools is a simple Flask web application that allows users to create and manage simple projects and save them within their account. Once a user creates a new account they are brought to a homepage that will be an empty table of projects. The user will notice that the header of the page greets them with **Hello, [username]** in the top left to ensure they know they are logged in with that username. This is also the button to click to come back to the homepage with the table of their projects. The other buttons the user will see are *New Project* and *Delete Projects*, we will get to those shortly. 

They can then click on the *New Project* link to create their first project. In New Project they will see a form that can be filled out to name the project, describe the project, enter the start date and enter the end date for the project. When they click the *Create Project* button the user will then be redirected back to their homepage where they will now see the project in the table of projects on their account. In the background, the application automatically assigns 3 fields; Phase, % Complete, and Status with the values Initiating, 0%, and Green respectively. This is because at the time of creating a project the standard is that these will always be the values for those fields. 

Now that the user has a project they can then begin to start adding tasks to the project. They can click on the name of the project and will be brought to the *Edit Project* page. This page has two sections, Project and Tasks. In the project section the user can make updates to any of the project fields to update the status if it ever changes from Green to Yellow or Red, and move along the Percent Complete and Phase the project is worked on. In the Tasks section, the user will see a table that initially has a blank form to add their first task. They can fill in all the fields to name the task, describe the task, assign the task to who needs to complete it, set the state of the task (Pending is default and others include Work In Progress, Closed Complete, and Closed Skipped), and set the start and end dates for the task. Once the user clicks *Add Task* they will see the task added above the blank form in another form that will allow them to Update the task as it is worked on and if the dates need to change. Once multiple tasks are added the user will notice that tasks are ordered by the End Date so the task that is due the earliest shows up first.

The user can also navigate to the *Delete Projects* link. This link shows the same table of their proejcts with a *Delete* button next to each project. This will allow the user to delete projects and their associated tasks if they are no longer needed. The user will see a confirmation message when they click delete to ensure they are making the correct choice. 

### Files created for PM Tools

#### app.py
Every Flask application has its app.py file that brings the app to life! Here is the breakdown of what is in my app.py:

##### Headers and Initalizing code
I utilized CS50's SQL library to assist with working with the database I created for this project. I imported libraries from flask and flask_session to assist with handling user sessions and all the rendering and redirecting I needed to do. I imported from werkzeug.security the ability to hash and check the hash for user passwords so I am not storing the password directly and it is more secure

I call helpers (more on that next) with a couple functions that are used throughout. I configured the application, configured sessions for when users login, and configured the database

##### Index

Index.html is the homepage the user is directed to when they login. It, like all other routes with @login_required, gets the user from the session to display in the top left of the page. The route then calls the db for the list of proejcts that user has created, looks for the POST method to redirect to the edit proejcts page, and returns index.html if accessed via GET.

##### Login

Login clears any sessions that may be active and then performs checks on the form fields to ensure the user has entered credentials that match in the database. Once those checks are complete, the user is redirected to their homepage described directly above.

##### Logout

Simply clear all sessions and redirect back to home which will be the login page.

##### Register

Register clears any sessions running and then performs checks on all the fields to ensure username is entered and doesn't match any current usernames, password and confirmation are entered and matched. Once those checks are complete the password is hashed in order to not store the password directly and the account is created. The user is redirected to the login to login with their new credentials.

##### New Project

New project allows the user to create a new project on their account. They will fill in the fields with name, description, start and end dates. The final fields of Phase, Status, and Percent Complete are autofilled with default values. The user is then redirected back to the homepage where they will see their new project.

##### Delete Project

Delete project allows the user to remove any projects and the associated tasks by clicking the *Delete* button. They will be prompted to confirm this is what they would like to do since this actions deletes from the databases. 

##### Edit Project

Edit project allows the user to edit the currently selected project and all associated tasks. The top section allows the user to updated any of the project fields as the project is moving along and commit those updates by clicking *Update Project*. The user can edit any tasks that are currently created and commit those updates by clicking *Update* next to the task. The user can then add new tasks in the bottom field and commit the new task by clicking *Add Task*.

#### helpers.py

Helpers contains two functions used throughout the app. Apology is how I render an error message when the user does not use the app as intended, such as not filling in a field when logging in. The other function, login_required, checks the session to ensure a user is logged in to be able to grab their data from the databases.

#### styles.css

Two simple formatting functions in this file help for branding the nav bar and font colors therein.

#### HTML files

##### layout.html

The general layout of the web app. This layout utilizes Bootstrap 5 for formatting. The navbar layout is a conditional based on whether a user is logged in or not, and utilizes Jinja to extend the layout of the title and main blocks of the web app.

##### index.html

The homepage of the user with the list of all their projects. Utilizes a for loop to grab the users projects from the database and returns their data for each of the fields. It also turns the name of the project into a button that allows the user to click and view the details of the project and tasks to be able to update them.

##### new_project.html

This page displays a simple form for the user to fill out to create a new project. Once the button is clicked they are redirected back to the homepage and will see all proejcts plus the new project created.

##### delete_project

A similar list to the homepage with a delete button next to each project. If clicked, the user is prompted with a message to confirm their choice. When confirmed, the project and all associated tasks are deleted from the corresponding databases.

##### edit_project

The page where most of the time will be spent. The top project section will show a form of the project with all details prefilled. The user can update any of these fields and use the Update Project button to commit those changes. The bottom Tasks sections has lines of forms with the first forms being all the current created tasks, ordered by end date. The user can update these fields similar to project above, and commit with the Update button. The final form is to create a new task and once created will be added to the list above.

#### projects.db

The database for the web app. Structured with 3 tables (users, projects, tasks). Users houses all the username and password hash data with a primary key id field. Projects houses all projects created with a primary key id field and foreign key user_id field to associate the project with the users. Tasks houses all the tasks with a primary key id field and two foreign key user_id and project_id fields to associate the tasks with the users and projects they are a part of.