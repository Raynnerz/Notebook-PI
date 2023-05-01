import sqlite3
from populate_Alunosdb import tupla_alunos


#cur é cursor e con é connection
con = sqlite3.connect("DB_notebooks.db")
cur = con.cursor()

cur.execute("DROP TABLE Aluno");
cur.execute("DROP TABLE AlunoNotebook");
cur.execute("DROP TABLE Notebook");
cur.execute("DROP TABLE Funcionario");


cur.execute("CREATE TABLE Aluno("
            "ra TEXT NOT NULL PRIMARY KEY,"
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

cur.executemany("insert into Aluno values (?, ?, ?)", tupla_alunos)

con.commit()
#Checar DB:

cur.execute("SELECT * from Aluno")

rows = cur.fetchall()

for row in rows:
    print(row)
