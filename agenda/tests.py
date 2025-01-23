from rest_framework.test import APITestCase
from agenda.models import Agendamento
import json
from datetime import datetime, timezone
from django.utils import timezone as django_timezone

class TestListagemAgendamento(APITestCase):
    def test_listagem_vazia(self):
        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)
        self.assertEqual(data, [])
        
    def test_listagem_de_agendamentos_criados(self):
        Agendamento.objects.create(
            data_horario=django_timezone.make_aware(datetime(2022, 3, 15, 0, 0)),
            nome_cliente="Alice",
            email_cliente="alice@email.com",
            telefone_cliente="3464636363"
        )

        response = self.client.get("/api/agendamentos/")
        data = json.loads(response.content)

        agendamento_serializado = {
            "id": 1,
            "data_horario": "2022-03-15T00:00:00Z",
            "nome_cliente": "Alice",
            "email_cliente": "alice@email.com",
            "telefone_cliente": "3464636363"
        }

        self.assertEqual(data[0], agendamento_serializado)


class TestCriacaoAgendamento(APITestCase):
    def test_cria_agendamento(self):
        agendamento_request_data = {
            "data_horario": "2025-03-15T00:00:00Z",
            "nome_cliente": "Calebe",
            "email_cliente": "calebewerneck@hotmail.com",
            "telefone_cliente": "4545343435"
        }

        response = self.client.post("/api/agendamentos/", agendamento_request_data, format="json")
        self.assertEqual(response.status_code, 201)

        agendamento_criado = Agendamento.objects.get()
        self.assertEqual(
            agendamento_criado.data_horario,
            datetime(2025, 3, 15, tzinfo=timezone.utc)
        )
        self.assertEqual(agendamento_criado.nome_cliente, "Calebe")
