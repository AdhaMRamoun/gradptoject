from flask import Flask, render_template, request, redirect, session
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

def load_usernames():
    with open('data.txt', 'r') as f:
        usernames = [line.split(',')[0] for line in f]
    return usernames

@app.route('/')
def home():
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Perform login validation logic here
        # ...
        # Assuming login is successful, store username in session
        session['username'] = username

        return redirect('/dashboard')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect('/dashboard')

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        pin = request.form['pin']
        rand_str = request.form['rand_str']

        # Perform registration logic here
        # ...
        # Assuming registration is successful, store username in session
        session['username'] = username

        return redirect('/dashboard')

    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')

    usernames = load_usernames()

    return render_template('dashboard.html', username=session['username'], usernames=usernames)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)
