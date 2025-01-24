from typing import Iterable
from datetime import date, datetime, timedelta, timezone
from agenda.libs import brasil_api
from agenda.models import Agendamento

def get_horarios_disponiveis(data: date) -> Iterable[datetime]:
    """
    Retorna uma lista com objetos do tipo datetime cujas datas são o mesmo dia passado (data)
    e os horários são os horários disponíveis para aquele dia, conforme outros agendamentos existam.
    """
    # Verificar se a data é um feriado usando a API Brasil
    try:
        if brasil_api.is_feriado(data):
            return []  # Se for feriado, retorna lista vazia
    except ValueError as e:
        raise ValueError("Erro ao verificar feriado na API Brasil.") from e

    # Definir o início e o fim do expediente
    start = datetime(year=data.year, month=data.month, day=data.day, hour=9, minute=0, tzinfo=timezone.utc)
    end = datetime(year=data.year, month=data.month, day=data.day, hour=18, minute=0, tzinfo=timezone.utc)

    # Intervalo entre os horários disponíveis
    delta = timedelta(minutes=30)

    horarios_disponiveis = []

    while start < end:
        # Verificar se o horário já está ocupado
        if not Agendamento.objects.filter(data_horario=start).exists():
            horarios_disponiveis.append(start)
        start += delta

    return horarios_disponiveis