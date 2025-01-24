from rest_framework.test import APITestCase

class TestGetHorarios(APITestCase):
    def test_quando_data_e_feriado_retorna_lista_vazia(self):
        response = self.client.get("/api/horarios/?data=2022-12-25")
        self.assertEqual(response.json(), [])  # Use .json() aqui
        
    def test_quando_data_e_dia_comum_retorna_lista_com_horarios(self):
        response = self.client.get("/api/horarios/?data=2022-10-03")
        horarios = response.json()
        self.assertNotEqual(horarios, [])
        self.assertEqual(horarios[0], "2022-10-03T09:00:00Z")  # Primeiro horário
        self.assertEqual(horarios[-1], "2022-10-03T17:30:00Z")  # Último horário correto
