from rest_framework import generics
from agenda.models import Agendamento
from agenda.serializers import PrestadorSerializer
from agenda.serializers import AgendamentoSerializer
from rest_framework.decorators import api_view
from rest_framework import permissions
from django.contrib.auth.models import User
from agenda.utils import get_horarios_disponiveis

from datetime import datetime
from django.http import JsonResponse

from rest_framework.decorators import api_view
from django.http import JsonResponse
from datetime import datetime
from agenda.utils import get_horarios_disponiveis



"""
Qualquer cliente(autenticado ou não) seja capaz de criar um Agendamento
Apenas o prestador de servico pode visualizar os agendamentos em sua agenda
Apenas o prestador de servico pode manipular os sues agendamentos
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
        Retorna os agendamentos filtrados por username do prestador
        se fornecido como parâmetro de consulta.
        Caso contrário, retorna todos os agendamentos.
        """
        username = self.request.query_params.get("username", None)
        if username:
            # Filtra os agendamentos pelo username do prestador
            return Agendamento.objects.filter(prestador__username=username)
        return Agendamento.objects.all()


class AgendamentoDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    View para recuperar, atualizar e excluir agendamentos.
    """
    permission_classes=[IsPrestador]
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer


class PrestadorList(generics.ListAPIView):
    serializer_class = PrestadorSerializer
    queryset = User.objects.all()
    
    
    



@api_view(http_method_names=["GET"])
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
            # Tenta converter a data informada para o formato datetime
            data = datetime.fromisoformat(data).date()
        except ValueError:
            return JsonResponse({"error": "Formato de data inválido"}, status=400)
    
    # Chama a função que retorna os horários disponíveis
    horarios_disponiveis = sorted(list(get_horarios_disponiveis(data)))
    
    # Retorna a lista de horários disponíveis
    return JsonResponse(horarios_disponiveis, safe=False)

