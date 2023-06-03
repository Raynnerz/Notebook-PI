import csv
import secrets
import string

with open('lista_alunos_original.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    lista_geral=[]
    for row in reader:
        lista_geral.append(tuple(row))

def generate_password():
    characters = string.ascii_lowercase + string.digits
    password = ''.join(secrets.choice(characters) for i in range(6))
    return password

for tupla in lista_geral:
    senha = generate_password()
    print('%s,%s,%s' % (tupla[0], tupla[1], senha))