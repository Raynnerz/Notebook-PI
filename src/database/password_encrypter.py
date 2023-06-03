import csv
import bcrypt

with open('ras_alunos_senhas.csv', 'r') as csvfile:
    reader = csv.reader(csvfile)
    lista_geral=[]
    for row in reader:
        lista_geral.append(tuple(row))

def encrypt(password):
    password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
    return password_hash

# def valida_senha(senha_digitada, hash_senha):
#     return bcrypt.hashpw(senha_digitada.encode('utf-8'), hash_senha) == hash_senha

for tupla in lista_geral:
    senha_hash = encrypt(tupla[2].encode('utf-8'))
    print('%s,%s,%s' % (tupla[0], tupla[1], senha_hash.decode()))