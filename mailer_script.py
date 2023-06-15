import os 
import smtplib
from email.message import EmailMessage

import csv

nome_arquivo = "dados.csv"

lista_emails = []
lista_senhas = []

with open('src/database/ras_alunos_senhas.csv', 'r') as csvfile:
    leitor_csv = csv.reader(csvfile)
    
    
    for linha in leitor_csv:
        
        primeiro_item = linha[0] + "@maua.br"
        lista_emails.append(primeiro_item)
        
        terceiro_atributo = linha[2]
        lista_senhas.append(terceiro_atributo)


EMAIL_ADRESS = 'foo-email@gmail.com'
EMAIL_PASSWORD = 'foo-password'
for i in lista_senhas:
    msg = EmailMessage()
    msg['Subject'] = 'Login e senha para MauáNotebooks!'
    msg['From'] = 'foo-email@gmail.com'
    msg['To'] = lista_senhas[i]
    msg.set_content = ("sua senha é ", lista_senhas[i])

with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
    smtp.login(EMAIL_ADRESS, EMAIL_PASSWORD)
#    smtp.send_message(msg)


