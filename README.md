# Polle Project Manager
Polle Project Manager is a simple project management system that allows one to create and manage projects. Each project consists of tasks with deadlines and comments added by the project members.

Polle Project Manager has following features:
* User account management
    - The user can create an account
    - Registered users can log in
    - Logged in users can logout
    - Registered users can delete their account if they do not have active projects. Deleting an account does not delete the account from the database of the system but only hides it so that the same account name cannot be chosen by another user and so that comments added by the account remain in the projects
* Project management
    - Logged in users can create new projects. The user who created the project will be set as the manager of that project
    - Project manager can add and remove workers from the project
    - Project manager can pass the manager status to workers participating in the project
    - Project manager can add and remove tasks from the project. The tasks will have a title, description and a deadline
    - Project manager can change the deadline of the task
    - Project manager and workers of the project can add comments to the tasks of the project
    - Anyone can view a list of projects with information regarding their current and past workers and tasks with different statuses
    - Anyone can view a list of workers with information regarding the projects they manage or work in and tasks in those projects with different statuses

The latest version of Polle can be tested [here](https://polle.herokuapp.com/).
