
from datetime import date
import requests
import logging

from django.conf import settings


def is_testing(date:date):
    logging.info(f"Fazer requisição para BrasilAPI para a data:{date.isoformat()}")
    if settings.TESTING == True:
        logging.info(f"Requisição nao esta sendo feita pois TESTING = True")
        if date.day == 25 and date.month ==12:
            return True
    return False    
        

def is_feriado(data:date) -> bool:

    
    ano=data.year
    r=requests.get(f"https://brasilapi.com.br/api/feriados/v1/{ano}")
    if not  r.status_code ==200:
        logging.info(f"Algum erro ocorreu na Brasil API")
        raise ValueError("Não foi posssivel consultar os feriados")
    feriados = r.json()
    for feriado in feriados:
        data_formatada = feriado["date"]
        data_feriado = date.fromisoformat(data_formatada)
        if data == data_feriado:
            return True
    return False    
    
    
    