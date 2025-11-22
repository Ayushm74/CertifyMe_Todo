from flask import Flask, render_template, redirect, url_for, session, request, flash
from models import db, User, Todo
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///certifyme.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from flask import g
@app.before_request
def before_request():
    g.user = None
    if 'user_id' in session:
        g.user = User.query.get(session['user_id'])

@app.route('/')
def home():
    return redirect(url_for('login'))

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email'].lower().strip()
        password = request.form['password']
        if not name or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('register.html')
        user = User(name=name, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful.', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid email or password.', 'error')
        return render_template('login.html')
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

# Forgot Password Route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email'].lower().strip()
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('No account found with that email.', 'error')
            return render_template('forgot_password.html')
        session['reset_user_id'] = user.id
        return redirect(url_for('reset_password'))
    return render_template('forgot_password.html')

# Reset Password Route (direct, after forgot)
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    reset_user_id = session.get('reset_user_id')
    if not reset_user_id:
        flash('Unauthorized access to password reset.', 'error')
        return redirect(url_for('forgot_password'))
    user = User.query.get(reset_user_id)
    if not user:
        flash('Unable to reset password.', 'error')
        return redirect(url_for('forgot_password'))
    if request.method == 'POST':
        password = request.form['password']
        if not password or len(password) < 4:
            flash('Password must be at least 4 characters.', 'error')
            return render_template('reset_password.html')
        user.set_password(password)
        db.session.commit()
        session.pop('reset_user_id')
        flash('Password has been reset. You may log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html')

# Dashboard Route (protected)
@app.route('/dashboard')
def dashboard():
    if not g.user:
        flash('Please log in to access the dashboard.', 'error')
        return redirect(url_for('login'))
    todos = Todo.query.filter_by(user_id=g.user.id).all()
    return render_template('dashboard.html', user=g.user, todos=todos)

# Add Todo (POST)
@app.route('/add_todo', methods=['POST'])
def add_todo():
    if not g.user:
        return redirect(url_for('login'))
    content = request.form['content'].strip()
    if not content:
        flash('Todo content cannot be empty.', 'error')
        return redirect(url_for('dashboard'))
    todo = Todo(content=content, user_id=g.user.id)
    db.session.add(todo)
    db.session.commit()
    flash('Todo added.', 'success')
    return redirect(url_for('dashboard'))

# Delete Todo (POST)
@app.route('/delete_todo/<int:todo_id>', methods=['POST'])
def delete_todo(todo_id):
    if not g.user:
        return redirect(url_for('login'))
    todo = Todo.query.filter_by(id=todo_id, user_id=g.user.id).first()
    if not todo:
        flash('Todo not found or not authorized.', 'error')
        return redirect(url_for('dashboard'))
    db.session.delete(todo)
    db.session.commit()
    flash('Todo deleted.', 'success')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
