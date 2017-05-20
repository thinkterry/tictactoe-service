from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    """Serialize model as JSON."""

    class Meta:
        """Map serializer fields to model fields."""

        model = Game
        fields = ('id', 'board')
