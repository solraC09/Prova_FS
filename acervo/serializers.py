from rest_framework import serializers
from .models import Livro
from datetime import date

ano_atual = date.today().year

class LivroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Livro
        fields = ["id", "titulo", "autor", "ano", "tipo", "categoria"]
        
    def validate_ano(self, value):
        if value > ano_atual:
            raise serializers.ValidationError(
                "N chegamos nesse ano"
            )
        return value