from rest_framework.test import APITestCase
from unittest import mock

class TestGetHorarios(APITestCase):
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)
    def test_quando_data_e_feriado_retorna_lista_vazia(self, _):
        response = self.client.get("/api/horarios/?data=2022-12-25")
        self.assertEqual(response.json(), [])  # Retorna lista vazia em feriados

    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self, _):
        response = self.client.get("/api/horarios/?data=2022-12-25")
        horarios = response.json()

        # Verifica se a lista não está vazia
        self.assertNotEqual(horarios, [])

        # Verifica se o primeiro e o último horários estão corretos
        self.assertEqual(horarios[0], "2022-12-25T09:00:00Z")  # Primeiro horário esperado
        self.assertEqual(horarios[-1], "2022-12-25T17:30:00Z")  # Último horário esperado
