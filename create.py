import sqlite3

#cur é cursor e con é connection
con = sqlite3.connect("DB_notebooks.db")
cur = con.cursor()

cur.execute("DROP TABLE Aluno");
cur.execute("CREATE TABLE Aluno("
            "ra INTEGER NOT NULL PRIMARY KEY,"
            "nome TEXT,"
            "senha TEXT)")

cur.execute("CREATE TABLE Notebook (idNotebook INTEGER NOT NULL PRIMARY KEY, bloco TEXT)")

cur.execute("CREATE TABLE AlunoNotebook("
            "idAlunoNotebook INTEGER NOT NULL PRIMARY KEY, "
            "ra INTEGER NOT NULL, "
            " idNotebook INTEGER NOT NULL, "
            "dataRetirada TEXT,"
            "dataDevolucao TEXT,"
            "FOREIGN KEY(ra) REFERENCES Alunos(ra),"
            "FOREIGN KEY(idNotebook) REFERENCES Notebook(idNotebook))")

cur.execute("CREATE TABLE Funcionario (idFuncionario INTEGER NOT NULL PRIMARY KEY, nome TEXT, senha TEXT)")