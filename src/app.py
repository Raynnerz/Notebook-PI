#autual
import sqlite3
from flask import Flask, jsonify, render_template, redirect, url_for, request, session
import time
app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')



@app.route('/home_aluno')
def home_aluno():
    return render_template('telaInicialAluno.html')


@app.route('/home_funcionario')
def home_funcionario():
    return render_template('telaListaAutentFuncionario.html')


@app.route('/update_requests_devolver')
def tela_aluno_devolver():
    if 'user_id' in session:
        session['username'] = session['user_id']
        return render_template('telaAlunoDevolver.html', username=session['username'])
    else:
        return "Unauthorized access"




@app.route('/update_requests_devolver', methods=['POST'])
def update_requests_devolver():
    if 'user_id' in session:

        username = session['user_id']

        conn = sqlite3.connect('src/database/DB_notebooks.db')
        cursor = conn.cursor()
        
        query= ("UPDATE AlunoNotebook SET request = 1 WHERE ra = ?")
        cursor.execute(query, (username,))
        conn.commit()

        conn.close()

        return "Request updated successfully"
    else:
        return "Unauthorized access"
    
    

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['ra']
        password = request.form['senha']
        session['user_id'] = username
        conn = sqlite3.connect('src/database/DB_notebooks.db')
        cursor = conn.cursor()

        query_aluno = "SELECT * FROM Aluno WHERE ra = ? AND senha = ?"
        cursor.execute(query_aluno, (username, password))
        aluno = cursor.fetchone()

        if aluno:
            session['user_id'] = aluno[0]
            conn.close()
            return redirect(url_for('home_aluno'))

        query_funcionario = "SELECT * FROM Funcionario WHERE nome = ? AND senha = ?"
        cursor.execute(query_funcionario, (username, password))
        funcionario = cursor.fetchone()

        if funcionario:
            session['user_id'] = funcionario[0]
            conn.close()
            return redirect(url_for('home_funcionario'))

        conn.close()
        error = 'Invalid username or password'
        return render_template('login_page.html', error=error)

    else:
        return render_template('login_page.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('login'))
    else:
        return render_template('welcome.html')


@app.route('/aluno_notebook', methods=['POST'])
def aluno_notebook():
    if 'user_id' in session:
        if request.method == 'POST':
            username = session['user_id']
            notebook_number = request.form['notebook_number']
            bloco = request.form['bloco']
            request_value = True
            conn = sqlite3.connect('src/database/DB_notebooks.db')
            cursor = conn.cursor()

            cursor.execute("SELECT MAX(idAlunoNotebook) FROM AlunoNotebook")
            result = cursor.fetchone()
            max_id = result[0]
            if max_id is None:
                max_id = 0
            idAlunoNotebook = max_id + 1

            query = "INSERT INTO AlunoNotebook (idAlunoNotebook, ra, idNotebook, bloco, request) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (idAlunoNotebook, username, notebook_number, bloco, request_value))
            conn.commit()

            conn.close()

            return redirect(url_for('update_requests_devolver'))
    else:
        return redirect(url_for('home_aluno'))

#aba Pendências
@app.route('/get_pendencies', methods=['GET'])
def get_pendencies():
    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()

    query = "SELECT * FROM AlunoNotebook WHERE DataRetirada IS NOT NULL AND request = 0"
    cursor.execute(query)

    requests = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    conn.close()

    return jsonify(requests)

#aba pedidos
@app.route('/get_requests_admin', methods=['GET'])
def get_requests_admin():
    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()

    query = "SELECT * FROM AlunoNotebook WHERE request = 1 AND DataDevolucao IS NULL"
    cursor.execute(query)

    requests = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(requests)

#aba pedidos
@app.route('/get_historico_admin', methods=['GET'])
def get_historico_admin():
    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()

    query = "SELECT * FROM AlunoNotebook WHERE request = 1 AND DataDevolucao IS NOT NULL"
    cursor.execute(query)

    requests = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    conn.close()

    return jsonify(requests)
#inserir info no BD com data

""" 
@app.route('/update_request', methods=['POST'])
def update_request():
    request_id = request.form.get('requestId')

    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM AlunoNotebook WHERE idAlunoNotebook = ?", (request_id,))
    row = cursor.fetchone()

    if row:
        status = [6]
        data_retirada = row[4]
        data_devolucao = row[5]

    if status == '0':
        if data_retirada != None and data_devolucao == None: 
            current_time = int(time.time())  
            query = "UPDATE AlunoNotebook SET request = 0, DataRetirada = ? WHERE idAlunoNotebook = ?"
            cursor.execute(query, (current_time, request_id))
            conn.commit()
            conn.close()
        elif data_retirada!= None and data_devolucao != None:
            current_time = int(time.time())  
            query = "UPDATE AlunoNotebook SET request = 0, DataDevolucao = ? WHERE idAlunoNotebook = ?"
            cursor.execute(query, (current_time, request_id))
            conn.commit()
            conn.close()



    return 'Request updated successfully'
"""

@app.route('/update_request', methods=['POST'])
def update_request():
    request_id = request.form.get('requestId')
    status = request.form.get('status')

    print(request_id, status)
    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM AlunoNotebook WHERE idAlunoNotebook = ?", (request_id,))
    row = cursor.fetchone()

    if row:
        data_retirada = row[4]
        data_devolucao = row[5]

        print(f'status: {status}\n ,data_devolucao: {data_devolucao}\n, data_retirada: {data_retirada}')
        
    if data_retirada == None:
        current_time = int(time.time())   
        query = "UPDATE AlunoNotebook SET request = ?, dataRetirada = ? WHERE idAlunoNotebook = ?"
        cursor.execute(query, (status, current_time, request_id))

    else: 
        current_time = int(time.time())  
        query = "UPDATE AlunoNotebook SET request = ?, dataDevolucao = ? WHERE idAlunoNotebook = ?"
        cursor.execute(query, (status, current_time, request_id))


    conn.commit()
    conn.close()


    return 'Request updated successfully'

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True, debug=True)
