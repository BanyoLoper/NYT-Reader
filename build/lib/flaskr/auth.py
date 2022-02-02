# Blueprint for authentication.
import functools
from textwrap import wrap

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

# View code for registration
@bp.route('register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            try:
                # Using placeholders and let the library take care of escaping the
                # Values, so we are not vulnerable to a SQL injenction attack
                db.execute(
                    "INSERT INTO user  (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                # url_for makes the url directly from the name of the parameter
                return redirect(url_for("auth.login"))
        flash(error)

    return render_template('auth/register.html')

# View for loging
@bp.route('/login', methods=('POST', 'GET'))
def login():
    if request.method == 'POST':
        print('Entrando')
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        print(username, password, user)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
    
        flash(error)
    return render_template('auth/login.html')

# If user has already logged in, loaded the info and make available to other viewers.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone

# Loggout deleting the user_id from the session
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# Check for each view the user logged in requirement.
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        
        return view(**kwargs)

    return wrapped_view