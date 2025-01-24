from django.urls import path
from agenda.views import AgendamentoList,AgendamentoDetail,PrestadorList,get_horarios

urlpatterns = [
    path('agendamentos/', AgendamentoList.as_view(), name='agendamento-list'),
    path('agendamentos/<int:pk>/', AgendamentoDetail.as_view(), name='agendamento-detail'),
    path('prestadores/', PrestadorList.as_view(), name='prestador-list'),
    path('horarios/', get_horarios, name='get-horarios'),  # Nova URL para a lista de horários
]
