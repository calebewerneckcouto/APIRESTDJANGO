# Importa a classe de teste do Django REST Framework para criar testes de API
# Importa a biblioteca de mocks do unittest para simular comportamentos
from rest_framework.test import APITestCase
from unittest import mock

# Define uma classe de teste para validar os horários retornados pela API
class TestGetHorarios(APITestCase):
    # Teste para verificar o comportamento quando a data fornecida é um feriado
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=True)  # Simula que a data é um feriado
    def test_quando_data_e_feriado_retorna_lista_vazia(self, _):
        # Faz uma requisição GET para o endpoint da API com uma data específica
        response = self.client.get("/api/horarios/?data=2022-12-25")
        
        # Verifica se a API retorna uma lista vazia, o comportamento esperado para feriados
        self.assertEqual(response.json(), [])  # O JSON retornado deve ser uma lista vazia

    # Teste para verificar o comportamento quando a data fornecida é um dia útil
    @mock.patch("agenda.libs.brasil_api.is_feriado", return_value=False)  # Simula que a data não é feriado
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self, _):
        # Faz uma requisição GET para o endpoint da API com uma data específica
        response = self.client.get("/api/horarios/?data=2022-12-25")
        
        # Obtém a resposta JSON como uma lista de horários
        horarios = response.json()

        # Valida que a lista de horários não está vazia
        self.assertNotEqual(horarios, [])

        # Verifica se o primeiro horário na lista está correto
        self.assertEqual(horarios[0], "2022-12-25T09:00:00Z")  # Horário esperado no início do expediente
        
        # Verifica se o último horário na lista está correto
        self.assertEqual(horarios[-1], "2022-12-25T17:30:00Z")  # Horário esperado no final do expediente
