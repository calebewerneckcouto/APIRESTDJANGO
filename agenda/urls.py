from django.urls import path
from agenda.views import AgendamentoList,AgendamentoDetail

urlpatterns = [
    path('agendamentos/',AgendamentoList.as_view()),
   path('agendamentos/<int:id>/',AgendamentoDetail.as_view(),name='agendamento-detail'),
]