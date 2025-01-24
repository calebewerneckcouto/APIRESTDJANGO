
from datetime import date
import requests

from django.conf import settings


def is_testing(date:date):
    if settings.TESTING == True:
        if date.day == 25 and date.month ==12:
            return True
    return False    
        

def is_feriado(data:date) -> bool:

    
    ano=data.year
    r=requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    if r.status_code !=200:
        raise ValueError("Não foi posssivel consultar os feriados")
    feriados = r.json()
    for feriado in feriados:
        data_formatada = feriado["date"]
        data_feriado = date.fromisoformat(data_formatada)
        if data == data_feriado:
            return True
    return False    
    
    
    