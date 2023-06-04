import sqlite3
import pytest


def test_clean_tables():
    con = sqlite3.connect("DB_notebooks_test.db")
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS Aluno")
    cur.execute("DROP TABLE IF EXISTS AlunoNotebook")
    cur.execute("DROP TABLE IF EXISTS Notebook")
    cur.execute("DROP TABLE IF EXISTS Funcionario")

def test_create_tables():
    con = sqlite3.connect("DB_notebooks_test.db")
    cur = con.cursor()

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
                "request BOOLEAN NOT NULL, "
                "FOREIGN KEY(ra) REFERENCES Alunos(ra), "
                "FOREIGN KEY(idNotebook) REFERENCES Notebook(idNotebook))")

    cur.execute("CREATE TABLE Funcionario (idFuncionario INTEGER NOT NULL PRIMARY KEY, nome TEXT, senha TEXT)")

    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cur.fetchall()

    assert set([t[0] for t in tables]) == set(['Aluno', 'Notebook', 'AlunoNotebook', 'Funcionario'])

    con.close()
    test_clean_tables()

def test_insert_alunos():
    con = sqlite3.connect('DB_notebooks_test.db')
    cur = con.cursor()

    cur.execute("CREATE TABLE Aluno("
                "ra TEXT NOT NULL PRIMARY KEY,"
                "nome TEXT,"
                "senha TEXT)")

    tupla_alunos_mock = [('12224843', 'Walter White', '123456'), ('22002100', 'Jessie Pinkman', '87654321')]
    cur.executemany("insert into Aluno values (?, ?, ?)", tupla_alunos_mock)

    cur.execute("SELECT COUNT(*) from Aluno")
    count = cur.fetchone()[0]

    assert count == 2

    con.close()
    test_clean_tables()


test_clean_tables()
test_create_tables()
test_insert_alunos()