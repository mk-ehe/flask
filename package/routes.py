from package import app, database
from flask import render_template, redirect, url_for, flash
from package.models import Item, User
from package.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required


@app.route('/')
def home_page():
    return render_template('home.html')


@app.route("/about")
def about_page():
    return render_template('home.html')


@app.route("/market")
@login_required
def market_page():
    items = Item.query.all()
    return render_template("market.html", items=items)


@app.route("/register", methods = ["GET", "POST"])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                                email = form.email.data.lower(),
                                password = form.password.data)
        
        database.session.add(user_to_create)
        database.session.commit()
        login_user(user_to_create)
        flash(f"Account Created Successfully!", category="success")
        return redirect(url_for("market_page"))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            for i in err_msg:
                flash(i, category="danger")

    return render_template("register.html", form=form)

@app.route("/login", methods = ["GET", "POST"])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():
        attempted_username = User.query.filter_by(username=form.username.data).first()
        if attempted_username and attempted_username.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_username)
            flash(f"Login successful!", category="success")
            return redirect(url_for("market_page"))
        
        else:
            flash("Wrong credentials, try again.", category="danger")
        
    return render_template("login.html", form=form)

@app.route("/logout")
def logout_page():
    logout_user()
    flash("Successfully logged out.", category="info")
    return redirect(url_for("home_page"))