from rest_framework import serializers
from agenda.models import Agendamento
from agenda.utils import get_horarios_disponiveis
from django.contrib.auth.models import User
from django.utils import timezone

# Serializador para o modelo Agendamento
class AgendamentoSerializer(serializers.ModelSerializer):
    # Campo do prestador sobrescrito para usar o username ao invés do objeto User
    prestador = serializers.CharField()  

    class Meta:
        # Define o modelo e os campos que serão serializados
        model = Agendamento
        fields = ['id', 'data_horario', 'nome_cliente', 'email_cliente', 'telefone_cliente', 'prestador']

    # Validação personalizada para o campo "prestador"
    def validate_prestador(self, value):
        try:
            # Tenta buscar o usuário pelo username
            prestador_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            # Levanta erro caso o usuário não exista
            raise serializers.ValidationError("username não existe!")
        return prestador_obj  # Retorna o objeto User para uso posterior

    # Validação personalizada para o campo "data_horario"
    def validate_data_horario(self, value):
        # Verifica se a data/hora do agendamento não está no passado
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
        # Verifica se o horário está disponível
        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError("Esse horário não está disponível!")
        return value

    # Validação geral para múltiplos campos
    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")
        # Regras de validação para e-mails brasileiros e números de telefone
        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
            raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")
        return attrs

    # Criação de um novo agendamento
    def create(self, validated_data):
        # Remove o campo prestador dos dados validados e utiliza o objeto User validado
        prestador = validated_data.pop("prestador")
        # Cria e retorna um novo objeto Agendamento
        agendamento = Agendamento.objects.create(
            prestador=prestador,
            data_horario=validated_data["data_horario"],
            nome_cliente=validated_data["nome_cliente"],
            email_cliente=validated_data["email_cliente"],
            telefone_cliente=validated_data["telefone_cliente"],
        )
        return agendamento

    # Atualização de um agendamento existente
    def update(self, instance, validated_data):
        # Atualiza os campos do objeto Agendamento
        instance.data_horario = validated_data.get("data_horario", instance.data_horario)
        instance.nome_cliente = validated_data.get("nome_cliente", instance.nome_cliente)
        instance.email_cliente = validated_data.get("email_cliente", instance.email_cliente)
        instance.telefone_cliente = validated_data.get("telefone_cliente", instance.telefone_cliente)
        
        # Atualiza o prestador, caso esteja nos dados validados
        if "prestador" in validated_data:
            instance.prestador = validated_data["prestador"]

        # Salva as alterações no banco de dados
        instance.save()
        return instance

# Serializador para o modelo User, representando o prestador
class PrestadorSerializer(serializers.ModelSerializer):
    # Inclui os IDs dos agendamentos relacionados ao prestador
    agendamentos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        # Define o modelo e os campos que serão serializados
        model = User
        fields = ['id', 'username', 'agendamentos']

    # Substitui o campo `agendamentos` para usar o serializador completo dos agendamentos
    agendamentos = AgendamentoSerializer(many=True, read_only=True)
