from rest_framework import mixins, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from django.http import JsonResponse


class AgendamentoList(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    generics.GenericAPIView,  # Corrigido: nome da classe
):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer

    def get(self, request, *args, **kwargs):
        # Retorna a lista de agendamentos
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        # Cria um novo agendamento
        return self.create(request, *args, **kwargs)

class AgendamentoDetail(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer
    lookup_field ="id"  # pode usar id agora se quiser
    def get(self, request, *args, **kwargs):
        # Retorna a lista de agendamentos
        return self.retrieve(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        # Atualiza total ou parcial
        return self.partial_update(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs):
        # Atualiza total
        return self.update(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        # Deleta os dados
        return self.destroy(request, *args, **kwargs)
    
    




