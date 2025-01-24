from rest_framework import generics
from agenda.models import Agendamento
from agenda.serializers import AgendamentoSerializer
from rest_framework.decorators import api_view
from rest_framework import permissions


"""
Qualquer cliente(autenticado ou não) seja capaz de criar um Agendamento
Apenas o prestador de servico pode visualizar os agendamentos em sua agenda
Apenas o prestador de servico pode manipular os sues agendamentos
"""


class AgendamentoList(generics.ListCreateAPIView):
    """
    View para listar e criar agendamentos.
    Permite filtragem de agendamentos pelo username do prestador.
    """
    serializer_class = AgendamentoSerializer
    permissions_classe=[permissions.IsAuthenticatedOrReadOnly]
    
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
    queryset = Agendamento.objects.all()
    serializer_class = AgendamentoSerializer



      