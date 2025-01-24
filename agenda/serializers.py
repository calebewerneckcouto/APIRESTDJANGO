from rest_framework import serializers
from agenda.models import Agendamento
from agenda.utils import get_horarios_disponiveis

from django.contrib.auth.models import User
from django.utils import timezone


class AgendamentoSerializer(serializers.ModelSerializer):
    prestador = serializers.CharField()  # Sobrescreve para usar o username

    class Meta:
        model = Agendamento
        fields = ['id', 'data_horario', 'nome_cliente', 'email_cliente', 'telefone_cliente', 'prestador']

    def validate_prestador(self, value):
        try:
            prestador_obj = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("username não existe!")
        return prestador_obj  # Retorna o objeto User

    def validate_data_horario(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Agendamento não pode ser feito no passado!")
        if value not in get_horarios_disponiveis(value.date()):
            raise serializers.ValidationError("Esse horário nao esta disponivel!")
        return value

    def validate(self, attrs):
        telefone_cliente = attrs.get("telefone_cliente", "")
        email_cliente = attrs.get("email_cliente", "")
        if email_cliente.endswith(".br") and telefone_cliente.startswith("+") and not telefone_cliente.startswith("+55"):
            raise serializers.ValidationError("E-mail brasileiro deve estar associado a um número do Brasil (+55)")
        return attrs

    def create(self, validated_data):
        prestador = validated_data.pop("prestador")  # Remove e utiliza o objeto User validado
        agendamento = Agendamento.objects.create(
            prestador=prestador,
            data_horario=validated_data["data_horario"],
            nome_cliente=validated_data["nome_cliente"],
            email_cliente=validated_data["email_cliente"],
            telefone_cliente=validated_data["telefone_cliente"],
        )
        return agendamento

    def update(self, instance, validated_data):
        instance.data_horario = validated_data.get("data_horario", instance.data_horario)
        instance.nome_cliente = validated_data.get("nome_cliente", instance.nome_cliente)
        instance.email_cliente = validated_data.get("email_cliente", instance.email_cliente)
        instance.telefone_cliente = validated_data.get("telefone_cliente", instance.telefone_cliente)

        # Atualização do prestador (se necessário)
        if "prestador" in validated_data:
            instance.prestador = validated_data["prestador"]

        instance.save()
        return instance


class PrestadorSerializer(serializers.ModelSerializer):
    agendamentos = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'agendamentos']
        
    agendamentos = AgendamentoSerializer(many=True,read_only=True)    
