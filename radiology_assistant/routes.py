from radiology_assistant import app
from flask import render_template

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/admin")
def admin():
    return render_template("admin.html")