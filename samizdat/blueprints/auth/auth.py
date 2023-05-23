from flask import Blueprint, render_template, request, url_for, redirect, flash
from sqlalchemy import exc
from werkzeug.security import generate_password_hash, check_password_hash

from samizdat.forms import RegistrationForm, LoginForm
from samizdat.db import session
from samizdat.models import User

bp = Blueprint('auth', __name__,
               template_folder='templates')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                user = User()
                user.name = username
                user.email = email
                user.password = generate_password_hash(password)
                session.add(user)
                session.commit()
            except exc.SQLAlchemyError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        error = None
        user = session.query(User).filter(User.name == username).first()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            session.flush()
            return redirect(url_for('blog.index'))

        flash(error)

    return render_template('auth/login.html')
