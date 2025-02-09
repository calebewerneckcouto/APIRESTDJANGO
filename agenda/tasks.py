import csv
from io import StringIO
from django.core.mail import EmailMessage
from agenda.serializers import PrestadorSerializer
from django.contrib.auth.models import User
from tamarcado.celery import app
from celery import shared_task
from django.core.mail import EmailMessage
import base64
import json
import requests
from django.core.mail import EmailMessage
from dotenv import load_dotenv
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Attachment, FileContent, FileName, FileType, Disposition



load_dotenv()
@app.task
def gera_relatorio_prestadores():
    print("Iniciando geração de relatório...")  # Log de depuração

    output = StringIO()
    writer = csv.writer(output)
    
    # Escrevendo cabeçalhos no CSV
    writer.writerow([
        "prestador",
        "data_horario",
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
    ])

    # Obtendo os prestadores
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)

    # Iterando sobre os prestadores e agendamentos
    for prestador in serializer.data:
        print(f"Processando prestador: {prestador}")  # Log de depuração
        for agendamento in prestador.get("agendamentos", []):
            print(f"Adicionando agendamento: {agendamento}")  # Log de depuração
            writer.writerow([
                agendamento["prestador"],
                agendamento["data_horario"],
                agendamento["nome_cliente"],
                agendamento["email_cliente"],
                agendamento["telefone_cliente"],
            ])

    # Gerar o conteúdo do CSV
    csv_content = output.getvalue()
    
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    if not SENDGRID_API_KEY:
        print("Erro: A chave da API do SendGrid não foi encontrada no arquivo .env.")
        return

    # Dados do e-mail
    subject = 'Tamarcado - Relatório de prestadores'
    message = 'Em anexo o relatório solicitado'
    from_email = 'calebewerneck@gmail.com'
    to_email = ['calebewerneck@gmail.com']  # Destinatário
    filename = "relatorio_prestadores.csv"

    # Codificar o conteúdo CSV em base64 (necessário para anexos)
    encoded_csv = base64.b64encode(csv_content.encode('utf-8')).decode()

    # Criar o anexo utilizando os helpers do SendGrid
    attachment = Attachment(
        FileContent(encoded_csv),
        FileName(filename),
        FileType("text/csv"),
        Disposition("attachment")
    )

    # Criar o e-mail usando o helper Mail
    mail = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        plain_text_content=message  # ou html_content=message, se preferir
    )

    # Adicionar o anexo
    mail.attachment = attachment

    # Enviar o e-mail utilizando a API do SendGrid
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(mail)
        print(f"Status do envio: {response.status_code}")
        print("Relatório gerado e enviado com sucesso.")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")