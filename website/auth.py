from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Users, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
auth = Blueprint("auth", __name__)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('route.sign_in'))


@auth.route('/new_user', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('username')
        pass1 = request.form.get('password1')
        pass2 = request.form.get('password2')

        query = Users.query.filter_by(identifier=id).first()
        if query:
            flash(f'Hey {query.username}, your\'e already a user please sign in', category="error")
            return redirect(url_for('auth.sign_in'))
        elif pass1 != pass2:
            flash("password does not match", category="error")
        elif len(pass1) < 6:
            flash('password should contain atleast 6 words', category="error")
        else:
            new_user = Users(username=name, identifier=id, password=generate_password_hash(pass1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            flash('Account created', category="success")
            login_user(new_user, remember=True)
            return redirect(url_for('route.home'))
    return render_template("new_user.html")


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        id = request.form.get('id')
        password = request.form.get('password')
        query = Users.query.filter_by(identifier=id).first()
        if query:
            if check_password_hash(query.password, password):
                flash(f"welcome back {query.username}", category="success")
                login_user(query, remember=True)
                return redirect(url_for('route.home'))
            else:
                flash("Invalid password", category="error")
        else:
            flash("We couldn't find you please sign up", category="error")
            return redirect(url_for('auth.sign_up'))

    return render_template("sign_in.html")
