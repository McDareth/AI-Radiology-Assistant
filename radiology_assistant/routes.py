from radiology_assistant import app, bcrypt, db
from flask import render_template, redirect, url_for, flash, request, session
from flask_login import current_user, login_user, logout_user
from radiology_assistant.models import User
from radiology_assistant.forms import RegistrationForm, LoginForm, ImageUploadForm, ConfirmUploadForm
from radiology_assistant.utils import save_temp_image, image_in_temp

@app.route("/", methods=['GET', 'POST'])
def home():
    form = ImageUploadForm()
    if form.is_submitted():
        if form.validate():
            save_temp_image(form.image.data, 600)
            return redirect(url_for("confirm"))
        else:
            flash("Something went wrong. Please make sure you uploaded either a .png or .jpg image.", "danger")
    return render_template("home.html", form=form)

@app.route("/confirm", methods=['GET', 'POST'])
def confirm():
    
    if not image_in_temp():
        flash("You can't confirm an image until you upload an image!", "danger")
        return redirect(url_for("home"))
    else:
        form = ConfirmUploadForm()
        if form.is_submitted():
            return redirect(url_for("results"))
        else:
            return render_template("confirmation.html", img_name=session.get("temp_image"), form=form)

@app.route("/search")
def search():
    return render_template("search.html")

@app.route("/results")
def results():
    return render_template("results.html")

@app.route("/report")
def report():
    return render_template("report.html")

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(firstname=form.firstname.data, lastname=form.lastname.data, username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You may now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)
    # return render_template("register.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password and try again.', 'danger')
    return render_template('login.html', title='Login', form=form)
    # return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/admin")
def admin():
    return render_template("admin.html")