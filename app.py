from flask import Flask, render_template, request, redirect, url_for, session
from parser import parse_resume
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# ✅ PostgreSQL DB connection string (directly pasted here for now)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:khushi157802@db.ozcgapincdurbbmquspx.supabase.co:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# ✅ Initialize SQLAlchemy
db = SQLAlchemy(app)

# ✅ User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)

@app.route('/')
def home():
    return redirect(url_for('login'))

# ✅ SIGNUP Route — Save user to PostgreSQL
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "User already exists!"

        # Create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

# ✅ LOGIN Route — Check from PostgreSQL
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials"

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['user'])

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['resume']
        if file:
            filepath = f"./uploads/{file.filename}"
            file.save(filepath)
            parsed_data = parse_resume(filepath)
            return render_template('dashboard.html', data=parsed_data, username=session['user'])

    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
