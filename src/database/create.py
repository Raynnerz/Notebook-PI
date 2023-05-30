import sqlite3
from populate_student_schema import tupla_alunos


#cur é cursor e con é connection
con = sqlite3.connect("src/database/DB_notebooks.db")
cur = con.cursor()

#cur.execute("DROP TABLE Aluno");
cur.execute("DROP TABLE AlunoNotebook");
#cur.execute("DROP TABLE Notebook");
#cur.execute("DROP TABLE Funcionario");


#cur.execute("CREATE TABLE Aluno("
#            "ra TEXT NOT NULL PRIMARY KEY,"
#            "nome TEXT,"
#           "senha TEXT)")

#cur.execute("CREATE TABLE Notebook (idNotebook INTEGER NOT NULL PRIMARY KEY, bloco TEXT)")

cur.execute("CREATE TABLE AlunoNotebook("
            "idAlunoNotebook INTEGER NOT NULL PRIMARY KEY, "
            "ra INTEGER NOT NULL, "
            "idNotebook INTEGER NOT NULL, "
            "bloco CHARACTER(1) NOT NULL, "
            "dataRetirada TEXT, "
            "dataDevolucao TEXT, "
            "request BOOLEAN NOT NULL, "
            "FOREIGN KEY(ra) REFERENCES Alunos(ra), "
            "FOREIGN KEY(idNotebook) REFERENCES Notebook(idNotebook))")

#cur.execute("CREATE TABLE Funcionario (idFuncionario INTEGER NOT NULL PRIMARY KEY, nome TEXT, senha TEXT)")

#cur.executemany("insert into Aluno values (?, ?, ?)", tupla_alunos)

#cur.execute("insert into Funcionario values (?, ?, ?)", (0, 'admin', 'admin'))

#cur.executemany("insert into Notebook values (?, ?)", [(0, "U"),(1, "U"), (2, "H"), (3, "H"), (4, "U") ])
con.commit()

#cur.execute("SELECT * from Funcionario")

#rows = cur.fetchall()

#for row in rows:
#    print(row)
