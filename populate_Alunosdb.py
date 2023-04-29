import csv

with open('lista_alunos_original.csv', 'r') as csvfile:
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
    if numeric_chars:
        lista_ra_n.append(int(numeric_chars))
for j in lista_ra_n:
    j = str(j)
    lista_ra_n_invertida.append(j[::-1])

tupla_alunos = [(a, b, c) for (a, b), c in zip(lista_geral, lista_ra_n_invertida)]
print(tupla_alunos)
print(type(tupla_alunos))