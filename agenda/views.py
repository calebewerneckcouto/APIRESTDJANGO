from django.shortcuts import render
from rest_framework.decorators import api_view

from django.shortcuts import get_object_or_404
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from django.http import JsonResponse

# Create your views here.
@api_view(http_method_names=["GET"])
def agendamento_detail(request,id):
    obj=get_object_or_404(Agendamento,id=id)
    serializer =AgendamentoSerializer(obj)
    return JsonResponse(serializer)

@api_view(http_method_names=["GET"])
def agendamento_list(request):
    qs = Agendamento.objects.all()
    serializer =AgendamentoSerializer(qs,many=True)
    return JsonResponse(serializer.data,safe=False)