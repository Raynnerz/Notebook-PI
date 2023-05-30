import csv
import random

with open('src/database/students_list.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    lista_geral=[]
    for row in reader:
        lista_geral.append(tuple(row))

lista_ra = []
lista_ra_n = []
lista_ra_n_invertida = []
for i in lista_geral:
    lista_ra.append(i[0])
for element in lista_ra:
    numeric_chars = ''
    for char in element:
        if char.isdigit():
            numeric_chars += char
    str_listed_ra = list(numeric_chars)
    random.shuffle(str_listed_ra)
    numeric_chars = ''.join(str_listed_ra)

    if numeric_chars:
        lista_ra_n.append(int(numeric_chars))

tupla_alunos = [(a, b, c) for (a, b), c in zip(lista_geral, lista_ra_n)]

