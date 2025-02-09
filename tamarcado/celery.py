from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Definindo o módulo de configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tamarcado.settings.dev')

# Criando a instância do Celery
app = Celery('tamarcado')

app.config_from_object('django.conf:settings',namespace='CELERY')


# Descobrindo as tarefas automaticamente nas aplicações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregando as tarefas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
