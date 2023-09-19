import discord
from discord.ext import commands

from flask import Flask, request, jsonify
import imaplib
import email
from email.header import decode_header
from datetime import datetime
from auxfunc import formatHeader, KeyWordInMessage, notFindEmail


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

app = Flask(__name__)

@bot.event
async def on_ready():
    print('Bot conectado')


@bot.command(name='leads')
async def nome_funcao(ctx, args):
  emailDate = args
  with app.app_context():
    response = consultar_emails(emailDate)
    if(response):
      for item in response:
        LeadEmail = KeyWordInMessage(item, 'Identificador: home')
        #if(LeadEmail):
          #responseFormat = formatHeader(item)
          #await ctx.send(responseFormat)
        responseFormat = formatHeader(item)
        await ctx.send(responseFormat)
    else:
      responseFormat = notFindEmail()
      await ctx.send(responseFormat)
      

# CONSULTAR EMAILS
# Configurações do servidor IMAP do Gmail
IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993

#pessoa que enviou o email
remetente = "" 

# Informações da conta de e-mail
EMAIL = ''  # E-mail que quero buscar as informações
PASSWORD = ''  # Senha de App gerada pelo Google

TokenBot = ''


def consultar_emails(emailDate):

    # Conexão com o servidor IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)

    # Login
    mail.login(EMAIL, PASSWORD)

    # Selecionar a caixa de entrada (INBOX)
    mail.select("inbox")

    # Verficar quais emails buscar
    todos = "True"
    lidos = "False"
    nao_lidos = "False"

    statusMessage = (
        'ALL' if todos == "True" else
        'SEEN' if lidos == "True" else
        'UNSEEN' if nao_lidos == "True" else
        None
    )

    # Remetente
    senderFind = f'FROM "{remetente}"'

    # formatação de data
    senderOnDate = False
    if(emailDate):
      data_objeto = datetime.strptime(emailDate, '%d-%m-%Y')
      emailDate = data_objeto.strftime('%d-%b-%Y')
      senderOnDate = f"ON {emailDate}"
      print(senderOnDate)

  
    dataInicial  = False
    senderDateInital = False
    if(dataInicial):
        data_obj = datetime.strptime(dataInicial, "%Y-%m-%d")
        date = data_obj.strftime("%d-%b-%Y")
        senderDateInital = f"SINCE {date}"
        print(senderDateInital)

    dataFinal = False
    senderDateFinal = False
    if(dataFinal):
        data_obj = datetime.strptime(dataFinal, "%Y-%m-%d")
        date = data_obj.strftime("%d-%b-%Y")
        senderDateFinal = f"BEFORE {date}"
        print(senderDateFinal)

    # Buscar os e-mails
    if(senderDateInital and senderDateFinal): # Procura por gap data
        print('gap alternative')
        gap = f'{senderDateFinal} {senderDateFinal}'
        status, data = mail.search(None, statusMessage, senderFind, gap)
    elif (senderDateInital):
        print('inital alternative')
        status, data = mail.search(None, statusMessage, senderFind, senderDateInital)
    elif (senderDateFinal):
        print('final alternative')
        status, data = mail.search(None, statusMessage, senderFind, senderDateFinal)
    elif (senderOnDate):
        try:
          print('On Date alternative')
          status, data = mail.search(None, statusMessage, senderFind, senderOnDate)  
        except error:
          return False
    else: # Procura sem data
        print('none alternative')
        status, data = mail.search(None, statusMessage, senderFind)

    # Obter os números dos e-mails
    email_ids = data[0].split()

    # Inicializar uma lista para armazenar os detalhes dos e-mails
    email_details = []

    # Iterar sobre os e-mails
    for email_id in email_ids:
        # Buscar o e-mail pelo ID
        status, data = mail.fetch(email_id, "(RFC822)")

        # Obter o conteúdo do e-mail
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        # Decodificação de caracteres especiais
        try:
            subject = decode_header(email_message["Subject"])[0][0]
            decoded_text = subject.decode('utf-8')
        except:
            decoded_text = email_message["Subject"]

        # Separando nome e email do remetente
        nomeEmail = str(email_message["From"]).split("<")

        if email_message.is_multipart():
          for part in email_message.walk():
            if part.get_content_type() == "text/plain":
              emailMessage = part.get_payload(decode=True).decode()
              
        # Adicionar os detalhes do e-mail à lista
        email_details.append({
            'Email numero': int(email_id),
            'Remetente': nomeEmail[0].strip(),
            'Email': nomeEmail[1].strip(),
            'Assunto': decoded_text,
            'Data': email_message["Date"],
            'Message': emailMessage
        })

    #retorno dos emails
    print(email_details)
    return email_details
  
    # Fechar a conexão com o servidor IMAP
    mail.close()
    mail.logout()
  
bot.run(TokenBot)