from app import app, db
from flask import render_template, request, redirect, url_for, abort
from flask_login import login_user, logout_user, current_user
from app.models.tables import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email).first()

        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            return abort(401)

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
        
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        user = User(username, email, password)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for("login"))
        
    return render_template("register.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))