from rest_framework import generics
from agenda.models import Agendamento
from agenda.serializers import PrestadorSerializer, AgendamentoSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions
from django.contrib.auth.models import User
from agenda.utils import get_horarios_disponiveis
from datetime import datetime
from rest_framework.response import Response
import csv
from django.http import HttpResponse
from agenda.tasks import gera_relatorio_prestadores


"""
Qualquer cliente (autenticado ou não) seja capaz de criar um Agendamento.
Apenas o prestador de serviço pode visualizar os agendamentos em sua agenda.
Apenas o prestador de serviço pode manipular seus agendamentos.
"""


class IsOwnerOrCreateOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "POST":
            return True  # Qualquer um pode criar agendamentos
        username = request.query_params.get("username", None)
        return request.user.is_authenticated and request.user.username == username


class IsPrestador(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.prestador == request.user


class AgendamentoList(generics.ListCreateAPIView):
    """
    View para listar e criar agendamentos.
    Permite filtragem de agendamentos pelo username do prestador.
    """
    serializer_class = AgendamentoSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        Retorna os agendamentos filtrados por username do prestador,
        se fornecido como parâmetro de consulta.
        Caso contrário, retorna todos os agendamentos.
        """
        username = self.request.query_params.get("username", None)
        if username:
            return Agendamento.objects.filter(prestador__username=username)
        return Agendamento.objects.all()


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View para recuperar, atualizar e excluir agendamentos.
    """
    permission_classes = [IsPrestador]
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer


@api_view(["GET"])
@permission_classes([permissions.IsAdminUser])
def relatorio_prestadores(request):
    """
    Endpoint para gerar um relatório de prestadores em JSON ou CSV.
    """
    formato = request.query_params.get("formato")
    prestadores = User.objects.all()
    serializer = PrestadorSerializer(prestadores, many=True)

    if formato == "csv":
        result = gera_relatorio_prestadores.delay()
        return Response({"task_id": result.task_id})

    return Response(serializer.data)


@api_view(["GET"])
def get_horarios(request):
    """
    Endpoint para retornar os horários disponíveis de acordo com a data informada na query string.
    """
    data = request.query_params.get("data")

    # Se não for passada uma data, usa a data atual
    if not data:
        data = datetime.now().date()
    else:
        try:
            data = datetime.fromisoformat(data).date()
        except ValueError:
            return Response({"error": "Formato de data inválido"}, status=400)

    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))

    return Response(horarios_disponiveis)
