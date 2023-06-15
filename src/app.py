import sqlite3
import json
import traceback
import bcrypt
from flask import Flask, jsonify, render_template, redirect, url_for, request, session
import time

app = Flask(__name__)
app.secret_key = 'your_secrete_key'

@app.route('/home_aluno')
def home_aluno():
    return render_template('telaInicialAluno.html')

@app.route('/telaListaAutentFuncionario_pendencias')
def telaListaAutentFuncionario_pendencias():
    return render_template('telaListaAutentFuncionario_pendencias.html')

@app.route('/telaListaAutentFuncionario_pedidos')
def telaListaAutentFuncionario_pedidos():
    return render_template('telaListaAutentFuncionario_pedidos.html')

@app.route('/telaListaAutentFuncionario_historico')
def telaListaAutentFuncionario_historico():
    return render_template('telaListaAutentFuncionario_historico.html')


@app.route('/update_requests_devolver')
def tela_aluno_devolver():
    if 'user_id' in session:
        session['username'] = session['user_id']
        return redirect(url_for('tela_espera_aluno', username=session['username']))
    else:
        return "Unauthorized access"
    

@app.route('/tela_espera_aluno')

@app.route('/tela_espera_aluno')
def tela_espera_aluno():
    if 'user_id' in session:
        username = session['user_id']
        conn = sqlite3.connect('src/database/DB_notebooks.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM AlunoNotebook WHERE ra = ?", (username,))
        row = cursor.fetchone()

        if row[6] == 1:
            return render_template('telaEsperaAluno.html', status=1)
        else:
            return render_template('telaAlunoDevolver.html', status=0)

    return "Unauthorized access"

@app.route('/get_status')
def get_status():
    if 'user_id' in session:
        username = session['user_id']
        conn = sqlite3.connect('src/database/DB_notebooks.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM AlunoNotebook WHERE ra = ?", (username,))
        row = cursor.fetchone()

        status = row[6] if row else None

        conn.close()

        return jsonify({"status": status})
    else:
        return jsonify({"status": None})

@app.route('/update_requests_devolver', methods=['POST'])
def update_requests_devolver():

    if 'user_id' in session:
        
        username = session['user_id']
        
        conn = sqlite3.connect('src/database/DB_notebooks.db')
        cursor = conn.cursor()


        cursor.execute("SELECT * FROM AlunoNotebook WHERE ra = ?", (username,))
        row = cursor.fetchone()
        
    
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

        query_aluno = "SELECT * FROM Aluno WHERE ra = ?"
        cursor.execute(query_aluno, (username,))
        aluno = cursor.fetchone()

        if aluno and bcrypt.hashpw(password.encode('utf-8'), aluno[2].encode('utf-8')) == aluno[2].encode('utf-8'):
            session['user_id'] = aluno[0]
            conn.close()
            return redirect(url_for('home_aluno'))

        query_funcionario = "SELECT * FROM Funcionario WHERE nome = ? AND senha = ?"
        cursor.execute(query_funcionario, (username, password))
        funcionario = cursor.fetchone()

        if funcionario:
            session['user_id'] = funcionario[0]
            conn.close()
            return redirect(url_for('telaListaAutentFuncionario_pedidos'))

        conn.close()
        error = 'Usuário e/ou fhistosenha inválido(s)'
        return render_template('tela_login.html', error=error)

    else:
        return render_template('tela_login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))


@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/aluno_notebook', methods=['POST'])
def aluno_notebook():
    if 'user_id' in session:
        if request.method == 'POST':
            username = session['user_id']
            notebook_number = request.form['notebook_number']
            bloco = request.form['bloco']
            request_value = 1
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
@app.route('/get_pendencias', methods=['GET'])
def get_pendencias():
    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()

    query = """
    SELECT AlunoNotebook.idAlunoNotebook, Aluno.nome AS aluno, AlunoNotebook.idNotebook, AlunoNotebook.bloco, AlunoNotebook.dataRetirada, AlunoNotebook.dataDevolucao, AlunoNotebook.request
    FROM AlunoNotebook
    INNER JOIN Aluno ON AlunoNotebook.ra = Aluno.ra
    WHERE AlunoNotebook.request = 0 AND AlunoNotebook.datadevolucao IS NULL
    """
    cursor.execute(query)

    pending_requests = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]

    conn.close()

    return jsonify(pending_requests)



#aba pedidos
@app.route('/get_historico_admin', methods=['GET'])
def get_historico_admin():
    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()
    query = """
    SELECT AlunoNotebook.idAlunoNotebook, Aluno.nome AS aluno, AlunoNotebook.idNotebook, AlunoNotebook.bloco, AlunoNotebook.dataRetirada, AlunoNotebook.dataDevolucao, AlunoNotebook.request
    FROM AlunoNotebook
    INNER JOIN Aluno ON AlunoNotebook.ra = Aluno.ra
    WHERE AlunoNotebook.request = 0 AND AlunoNotebook.datadevolucao IS NOT NULL
    """
    cursor.execute(query)
    requests = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    print(requests)
   
    conn.close()

    return jsonify(requests)

#aba pedidos
@app.route('/get_requests_admin', methods=['GET'])
def get_requests_admin():
    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()
    query = """
    SELECT AlunoNotebook.idAlunoNotebook, Aluno.nome AS aluno, AlunoNotebook.idNotebook, AlunoNotebook.bloco, AlunoNotebook.dataRetirada, AlunoNotebook.dataDevolucao, AlunoNotebook.request
    FROM AlunoNotebook
    INNER JOIN Aluno ON AlunoNotebook.ra = Aluno.ra
    WHERE AlunoNotebook.request = 1 AND AlunoNotebook.datadevolucao IS NULL
    """
    cursor.execute(query)

    requests = [dict(zip([column[0] for column in cursor.description], row)) for row in cursor.fetchall()]
    
    conn.close()

    return jsonify(requests)
#inserir info no BD com data
@app.route('/update_request', methods=['POST'])
def update_request():
    request_id = request.form.get('requestId')
    status = request.form.get('status')

    conn = sqlite3.connect('src/database/DB_notebooks.db')
    cursor = conn.cursor()
    print(status)

    cursor.execute("SELECT * FROM AlunoNotebook WHERE idAlunoNotebook = ?", (request_id,))
    row = cursor.fetchone()
    if row:
        data_retirada = row[4]
        data_devolucao = row[5]

    if row[6]==2:
        query = "DELETE FROM AlunoNotebook WHERE request = ?"
        cursor.execute(query, (status))
    else:
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
    app.run(host='127.0.0.1', port='8000', threaded=True)