import csv
import sqlite3

with open('src/database/ras_alunos_hashs.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    lista_geral=[]
    for row in reader:
        lista_geral.append(tuple(row))

#cur é cursor e con é connection
con = sqlite3.connect("src/database/DB_notebooks.db")
cur = con.cursor()

cur.execute("DROP TABLE Aluno")
cur.execute("DROP TABLE AlunoNotebook")
cur.execute("DROP TABLE Notebook")
cur.execute("DROP TABLE Funcionario")


cur.execute("CREATE TABLE Aluno("
            "ra TEXT NOT NULL PRIMARY KEY,"
            "nome TEXT,"
            "senha TEXT)")

cur.execute("CREATE TABLE Notebook (idNotebook INTEGER NOT NULL PRIMARY KEY, bloco TEXT)")

cur.execute("CREATE TABLE AlunoNotebook("
            "idAlunoNotebook INTEGER NOT NULL PRIMARY KEY, "
            "ra TEXT NOT NULL, "
            "idNotebook INTEGER NOT NULL, "
            "bloco CHARACTER(1) NOT NULL, "
            "dataRetirada TEXT, "
            "dataDevolucao TEXT, "
            "request INTEGER NOT NULL, "
            "FOREIGN KEY(ra) REFERENCES Alunos(ra), "
            "FOREIGN KEY(idNotebook) REFERENCES Notebook(idNotebook))")

cur.execute("CREATE TABLE Funcionario (idFuncionario INTEGER NOT NULL PRIMARY KEY, nome TEXT, senha TEXT)")

cur.execute("insert into Funcionario values (?, ?, ?)", (0, 'admin', 'admin'))

cur.executemany("insert into Aluno values (?, ?, ?)", lista_geral)

cur.executemany("insert into Notebook values (?, ?)", [(0, "U"),(1, "U"), (2, "H"), (3, "H"), (4, "U") ])

con.commit()