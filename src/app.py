import sqlite3
from flask import Flask, render_template, redirect, url_for, request, session

app = Flask(__name__)
app.secret_key = 'your_secret_key'
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['ra']
        password = request.form['senha']

        conn = sqlite3.connect('database/DB_notebooks.db')
        cursor = conn.cursor()

        query = "SELECT * FROM Aluno WHERE ra = ? AND senha = ?"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            session['user_id'] = user[0]
            conn.close()
            return redirect(url_for('welcome'))
        else:
            conn.close()
            error = 'Invalid username or password'
            return render_template('tela_login.html', error=error)
    else:
        return render_template('tela_login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
