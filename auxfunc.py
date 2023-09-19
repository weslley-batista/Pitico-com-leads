def formatHeader(email_obj):
    formatted_email = f"---------------------------------------------\n"
    formatted_email += f"Email número: {email_obj['Email numero']}\n"
    formatted_email += f"Remetente: {email_obj['Remetente']}\n"
    formatted_email += f"Email: {email_obj['Email']}\n"
    formatted_email += f"Assunto: {email_obj['Assunto']}\n"
    formatted_email += f"Data: {email_obj['Data']}\n"
    formatted_email += f"Mensagem: {email_obj['Message']}"
    formatted_email += f"---------------------------------------------\n"
    return formatted_email

def KeyWordInMessage(email_obj, palavra_alvo):
    mensagem = f"{email_obj['Message']}".lower()
    palavra_alvo = palavra_alvo.lower()


    # Verificar se a palavra está na lista de palavras
    if palavra_alvo in mensagem:
        return True
    else:
        return False

def notFindEmail():
  formatted_error = f"---------------------------------------------\n"
  formatted_error += f"Não foi encontrado email na data pedida\n"
  formatted_error += f"---------------------------------------------\n"
  return formatted_error
  