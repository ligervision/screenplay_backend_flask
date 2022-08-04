from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User


@app.route('/') # Home view function
@app.route('/index')
@login_required
def index():
    screenplays = [
        {
            'author': {'username': 'george_lucas_1977'},
            'title': 'Star Wars: A New Hope',
            'logline': "A long time ago, in a galaxy far, far, away..."
        },
        {
            'author': {'username': 'george_lucas_1977'},
            'title': 'The Gate',
            'logline': 'The Gate has been closed. Earth''s masses, desperate and displaced, roil in the teeming desert as the final lockout from the MON Sectopolis has doomed them to a seething, hostile remnant of the natural wonders Eden once bestowed upon Man. As chaos reigns in the natural world outside, the petty narcisissim and insidious philosophy of the elites within the bubble of Mons Sectopolis dooms this supposed "select" caste to exploit one another to harrowing levels of brutality, while the galvanized masses outside coalesce under the heroic visionary leadership of our Protagonist(s). Will our heroes find a way through ''The Gate'' and save humanity before the Sectopolis escapes to the orbit of Mars?'
        }
    ]
    return render_template('index.html', title='Home', screenplays=screenplays)


@app.route('/login', methods=['GET', 'POST']) # Login view function
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    screenplays = [
        {
            'author': {'username': 'george_lucas_1977'},
            'title': 'Star Wars: A New Hope',
            'logline': "A long time ago, in a galaxy far, far, away..."
        },
        {
            'author': {'username': 'george_lucas_1977'},
            'title': 'The Gate',
            'logline': 'The Gate has been closed. Earth''s masses, desperate and displaced, roil in the teeming desert as the final lockout from the MON Sectopolis has doomed them to a seething, hostile remnant of the natural wonders Eden once bestowed upon Man. As chaos reigns in the natural world outside, the petty narcisissim and insidious philosophy of the elites within the bubble of Mons Sectopolis dooms this supposed "select" caste to exploit one another to harrowing levels of brutality, while the galvanized masses outside coalesce under the heroic visionary leadership of our Protagonist(s). Will our heroes find a way through ''The Gate'' and save humanity before the Sectopolis escapes to the orbit of Mars?'
        }
    ]
    return render_template('user.html', user=user, screenplays=screenplays)
