from flask import render_template
from flask import redirect, render_template, request

from app import app
from entities import Worker
from functions import *

@app.route("/")
def index():
    worker = Worker("username")
    testilista = ["Projekti 1"]
    all_workers = get_worker_list()

    return render_template("index.html", lista=testilista, user=worker, workers=all_workers)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form["name"]
        password = request.form["password"]
        retyped_password = request.form["re-typed password"]
        error_messages = get_worker_creation_error_messages(name, password, retyped_password)
        if error_messages:
            print(error_messages)
            return render_template("register.html", messages=error_messages)
        #supervisor_status_requested = request.form["supervisor status request"]
        create_worker(name, password)
        return redirect("/")