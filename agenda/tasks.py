import csv
from io import StringIO
from agenda.serializers import PrestadorSerializer
from django.contrib.auth.models import User
from tamarcado.celery import app
from celery import shared_task

@app.task
def gera_relatorio_prestadores():
    import csv
    from io import StringIO
    from agenda.serializers import PrestadorSerializer
    from django.contrib.auth.models import User
    
    print("Iniciando geração de relatório...")  # Log de depuração

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "prestador",
        "data_horario",
        "nome_cliente",
        "email_cliente",
        "telefone_cliente",
        
    ])

    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)

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

    print("Relatório gerado com sucesso:")
    print(output.getvalue())  # Exibir o CSV gerado



@shared_task
def soma(a, b):
    return a + b