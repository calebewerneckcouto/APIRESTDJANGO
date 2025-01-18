from django.shortcuts import render

from django.shortcuts import get_object_or_404
from agenda.models import Agendamento

# Create your views here.
def agendamento_detail(request,id):
    obj=get_object_or_404(Agendamento,id=id)