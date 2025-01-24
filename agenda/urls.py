from django.urls import path
from agenda.views import AgendamentoList, AgendamentoDetail, PrestadorList, get_horarios

# Definição das rotas da aplicação "agenda"
urlpatterns = [
    # Rota para listar ou criar agendamentos
    path('agendamentos/', AgendamentoList.as_view(), name='agendamento-list'),

    # Rota para visualizar, atualizar ou deletar um agendamento específico (identificado pelo ID)
    path('agendamentos/<int:pk>/', AgendamentoDetail.as_view(), name='agendamento-detail'),

    # Rota para listar os prestadores disponíveis
    path('prestadores/', PrestadorList.as_view(), name='prestador-list'),

    # Rota para obter os horários disponíveis
    path('horarios/', get_horarios, name='get-horarios'),
]
