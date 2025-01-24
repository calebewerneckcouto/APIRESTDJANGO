from typing import Iterable
from datetime import date, datetime, timedelta, timezone
from agenda.libs import brasil_api
from agenda.models import Agendamento

def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
    """
    Retorna uma lista de objetos datetime representando os horários disponíveis para agendamento
    no dia especificado. Os horários disponíveis são definidos de acordo com a disponibilidade
    (não conflitam com agendamentos existentes) e o expediente.

    :param data: Objeto date representando o dia para verificar os horários disponíveis.
    :return: Lista de objetos datetime correspondendo aos horários disponíveis.
    """
    # Verificar se a data é um feriado usando a API Brasil
    try:
        if brasil_api.is_feriado(data):  # Chama a API para verificar se a data é um feriado
            return []  # Se for feriado, nenhum horário está disponível
    except ValueError as e:
        # Tratar possíveis erros da API, como problemas de conexão ou dados inválidos
        raise ValueError("Erro ao verificar feriado na API Brasil.") from e

    # Definir o início do expediente (9h da manhã no UTC)
    start = datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=9,
        minute=0,
        tzinfo=timezone.utc
    )

    # Definir o fim do expediente (18h no UTC)
    end = datetime(
        year=data.year,
        month=data.month,
        day=data.day,
        hour=18,
        minute=0,
        tzinfo=timezone.utc
    )

    # Intervalo entre os horários disponíveis (30 minutos)
    delta = timedelta(minutes=30)

    # Lista para armazenar os horários disponíveis
    horarios_disponiveis = []

    # Loop para verificar horários disponíveis no intervalo do expediente
    while start < end:
        # Verificar se o horário atual já está ocupado
        if not Agendamento.objects.filter(data_horario=start).exists():
            # Se o horário não está ocupado, adiciona à lista de horários disponíveis
            horarios_disponiveis.append(start)
        # Avança 30 minutos no tempo
        start += delta

    # Retorna a lista de horários disponíveis
    return horarios_disponiveis
