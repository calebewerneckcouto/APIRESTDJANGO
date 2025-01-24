from django.db import models

# Define o modelo de dados para o sistema de agendamentos
class Agendamento(models.Model):
    # Campo que representa o prestador de serviço
    # - É uma relação de chave estrangeira com o modelo de usuário padrão do Django (auth.User)
    # - `related_name="agendamentos"` permite acessar os agendamentos de um prestador pelo atributo `agendamentos`
    # - `on_delete=models.CASCADE` indica que, ao excluir o prestador, todos os agendamentos relacionados serão excluídos
    prestador = models.ForeignKey(
        'auth.User',  # Modelo de usuário padrão do Django
        related_name="agendamentos",  # Nome para acessar esta relação reversa
        on_delete=models.CASCADE  # Exclui os agendamentos ao excluir o prestador
    )

    # Campo que representa a data e o horário do agendamento
    # - Armazena informações de data e hora no formato `datetime`
    data_horario = models.DateTimeField()

    # Campo que armazena o nome do cliente
    # - É um texto com tamanho máximo de 200 caracteres
    nome_cliente = models.CharField(max_length=200)

    # Campo que armazena o e-mail do cliente
    # - Utiliza o tipo `EmailField`, que valida automaticamente se o valor inserido é um e-mail válido
    email_cliente = models.EmailField()

    # Campo que armazena o telefone do cliente
    # - Armazena o número de telefone como texto (máximo de 20 caracteres)
    telefone_cliente = models.CharField(max_length=20)

    # Classe Meta pode ser adicionada para configurações adicionais, como ordenação
    class Meta:
        verbose_name = "Agendamento"  # Nome singular para exibição no admin
        verbose_name_plural = "Agendamentos"  # Nome plural para exibição no admin
        ordering = ['data_horario']  # Ordena os agendamentos pela data e horário

    # Define a representação em texto do modelo
    def __str__(self):
        return f"{self.nome_cliente} - {self.data_horario}"  # Exibe o nome do cliente e a data do agendamento
