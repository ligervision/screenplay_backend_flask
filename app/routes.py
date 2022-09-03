from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User, Screenplay, Scene


# HOME
@app.route('/')
@app.route('/index')
@login_required
def index():
    screenplay = Screenplay.query.all()
    return render_template('index.html', title='Home', screenplay=screenplay)


# LOGIN
@app.route('/login', methods=['GET', 'POST'])
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
        flash(f"Welcome back, {user.username}!", "primary")
        return redirect(next_page)
    return render_template('login.html', title='Log In', form=form)


# LOGOUT
@app.route('/logout')
def logout():
    logout_user()
    flash('You have logged out of Screenplay', 'secondary')
    return redirect(url_for('index'))


# REGISTER
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'{user.username} has successfully registered!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


# VIEW USER
@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    screenplays = Screenplay.query.filter_by(user_id=current_user.id).order_by(Screenplay.screenplay_id.desc())
    return render_template('user.html', user=user, screenplay=screenplays)


# CREATE Screenplay
@app.route('/create/screenplay/', methods=('GET', 'POST'))
@login_required
def create_screenplay():
    # get form data
    if request.method == 'POST':
        title = request.form['title']
        logline = request.form['logline']
        dramatic_question = request.form['dramatic_question']
        genre1 = request.form['genre1']
        genre2 = request.form['genre2']
        genre3 = request.form['genre3']
        narrative_type = request.form['narrative_type']
        description = request.form['description']
        # create new instance
        new_screenplay = Screenplay(user_id=current_user.id,
                        title=title,
                        total_scenes=0,
                        logline=logline,
                        dramatic_question=dramatic_question,
                        genre1=genre1,
                        genre2=genre2,
                        genre3=genre3,
                        narrative_type=narrative_type,
                        description=description)
        db.session.add(new_screenplay)
        db.session.commit()
        flash(f"You have started a new screenplay, '{new_screenplay.title}'!", 'success')
        return redirect(url_for('view_screenplay', screenplay_id=new_screenplay.screenplay_id))
    return render_template('create/screenplay.html')


# READ Screenplay
@app.route('/screenplay/<int:screenplay_id>/')
@login_required
def view_screenplay(screenplay_id):
    screenplay = Screenplay.query.get_or_404(screenplay_id)
    scenes = Scene.query.filter_by(screenplay_id=screenplay.screenplay_id).order_by(Scene.scene_sequence)
    return render_template('screenplay/index.html', screenplay=screenplay, scene=scenes)


# UPDATE Screenplay
@app.route('/screenplay/<int:screenplay_id>/edit/', methods=('GET', 'POST'))
@login_required
def edit_screenplay(screenplay_id):
    screenplay = Screenplay.query.get_or_404(screenplay_id)

    # get form data
    if request.method == 'POST':
        title = request.form['title']
        logline = request.form['logline']
        dramatic_question = request.form['dramatic_question']
        genre1 = request.form['genre1']
        genre2 = request.form['genre2']
        genre3 = request.form['genre3']
        narrative_type = request.form['narrative_type']
        description = request.form['description']

        # edit - change table data
        screenplay.title = title
        screenplay.logline = logline
        screenplay.dramatic_question = dramatic_question
        screenplay.genre1 = genre1
        screenplay.genre2 = genre2
        screenplay.genre3 = genre3
        screenplay.narrative_type = narrative_type
        screenplay.description = description

        db.session.add(screenplay)
        db.session.commit()
        flash(f"'{screenplay.title}' has been updated!", 'success')
        return redirect(url_for('view_screenplay', screenplay_id=screenplay.screenplay_id))

    return render_template('screenplay/edit.html', screenplay=screenplay)


# DELETE Screenplay
@app.post('/screenplay/<int:screenplay_id>/delete/')
@login_required
def delete_screenplay(screenplay_id):
    screenplay = Screenplay.query.get_or_404(screenplay_id)
    db.session.delete(screenplay)
    db.session.commit()
    flash(f"'{screenplay.title}' has been deleted.", 'secondary')
    return redirect(url_for('user', username=current_user.username))


# CREATE Scene
@app.route('/screenplay/<int:screenplay_id>/create/scene/', methods=('GET', 'POST'))
@login_required
def create_scene(screenplay_id):
    current_screenplay = Screenplay.query.get_or_404(screenplay_id)
    last_scene_created = Scene.query.filter_by(screenplay_id=current_screenplay.screenplay_id).order_by(Scene.scene_sequence.desc()).first()
    new_scene_sequence = last_scene_created.scene_sequence + 1

    # get form data
    if request.method == 'POST':
        slugline = request.form['slugline']
        content = request.form['content']
        description = request.form['description']
        # Create new instance
        new_scene = Scene(screenplay_id=screenplay_id,
                        scene_index=new_scene_sequence,
                        scene_sequence=new_scene_sequence,
                        slugline=slugline,
                        content=content,
                        description=description,
                        plot_section='#')
        db.session.add(new_scene)
        db.session.commit()
        flash(f"You have created a new scene: '{new_scene.slugline}'!", 'success')
        return redirect(url_for('view_scene', scene_id=new_scene.scene_id))
    return render_template('create/scene.html', screenplay=current_screenplay)


# READ Scene
@app.route('/scene/<int:scene_id>/')
@login_required
def view_scene(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    screenplay = Screenplay.query.get_or_404(scene.screenplay_id)
    return render_template('scene/index.html', screenplay=screenplay, scene=scene)


# UDPATE Scene
@app.route('/scene/<int:scene_id>/edit/', methods=('GET', 'POST'))
@login_required
def edit_scene(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    screenplay_id = scene.screenplay_id
    current_screenplay = Screenplay.query.get_or_404(screenplay_id)

    # get form data
    if request.method == 'POST':
        slugline = request.form['slugline']
        content = request.form['content']
        description = request.form['description']

        # edit - change table data
        scene.slugline = slugline
        scene.content = content
        scene.description = description

        db.session.add(scene)
        db.session.commit()
        flash(f"'{scene.slugline}' has been updated!", 'success')
        return redirect(url_for('view_scene', scene_id=scene.scene_id))
    return render_template('scene/edit.html', scene=scene, screenplay=current_screenplay)
    
    
# DELETE Scene
@app.post('/scene/<int:scene_id>/delete/')
@login_required
def delete_scene(scene_id):
    scene = Scene.query.get_or_404(scene_id)
    db.session.delete(scene)
    db.session.commit()
    flash(f"'{scene.slugline}' has been deleted.", 'secondary')
    return redirect(url_for('view_screenplay', screenplay_id=scene.screenplay_id))
