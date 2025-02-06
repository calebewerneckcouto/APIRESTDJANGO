from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Definindo o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamarcado.settings.dev')

# Criando a instância do Celery
app = Celery('tamarcado')

# Configuração do broker do Celery
app.conf.broker_url = 'redis://default:0PKAZEkzurJg5aRpjSf3JiGhRDZQQg8Y@redis-13162.c241.us-east-1-4.ec2.redns.redis-cloud.com:13162/0'

# Definindo o backend para armazenar os resultados no Redis
app.conf.result_backend = 'redis://default:0PKAZEkzurJg5aRpjSf3JiGhRDZQQg8Y@redis-13162.c241.us-east-1-4.ec2.redns.redis-cloud.com:13162/0'

# Descobrindo as tarefas automaticamente nas aplicações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregando as tarefas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
