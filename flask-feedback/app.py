from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.widgets import PasswordInput
from models import db, User, Feedback
from secretpass import API_SECRET_KEY

app = Flask(__name__)
app.config['SECRET_KEY'] = API_SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()],  widget=PasswordInput(hide_value=False))
    email = StringField('Email', validators=[DataRequired(), Length(max=50)])
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=30)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=30)])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired()],  widget=PasswordInput(hide_value=False))

@app.route('/')
def index():
    """Redirects to register page"""
    return redirect(url_for('register'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Create a new user"""
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            first_name = form.first_name.data,
            last_name = form.last_name.data

        )
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect(url_for('secret'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login a user"""
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data,
        password = form.password.data,
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['username'] = user.username
            return redirect(url_for('/users/<username>'))
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout a user"""
    session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/users/<username>')
def user_profile(username):
    """Show user profile"""
    if 'username' in session and session['username'] == username:
        user = User.query.get(username)
        return render_template('user_profile.html', user=user)
    
@app.route('/users/<username>/delete')
def delete_user(username):
    """Delete user"""
    if 'username' in session and session['username'] == username:
        user = User.query.get(username)
        feedbacks = Feedback.query.filter_by(username=username).all()
        for feedback in feedbacks:
            db.session.delete(feedback)
        db.session.delete(user)
        db.session.commit()
        session.pop('username', None)
    return redirect(url_for('index'))

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    """Add feedback for user"""
    if 'username' in session and session['username'] == username:
        if request.method == 'POST':
            title = request.form['title']
            content = request.form['content']
            feedback = Feedback(title=title, content=content, username=username)
            db.session.add(feedback)
            db.session.commit()
            return redirect(url_for('user_profile', username=username))
        return render_template('add_feedback.html')
    return redirect(url_for('login'))

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Update feedback for user"""
    feedback = Feedback.query.get(feedback_id)
    if feedback and 'username' in session and session['username'] == feedback.username:
        if request.method == 'POST':
            feedback.title = request.form['title']
            feedback.content = request.form['content']
            db.session.commit()
            return redirect(url_for('user_profile', username=feedback.username))
        return render_template('update_feedback.html', feedback=feedback)
    return redirect(url_for('login'))

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get(feedback_id)
    if feedback and 'username' in session and session['username'] == feedback.username:
        db.session.delete(feedback)
        db.session.commit()
    return redirect(url_for('user_profile', username=feedback.username))
