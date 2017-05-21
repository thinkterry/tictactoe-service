import json
from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    """Serialize model as JSON."""

    class Meta:
        """Map serializer fields to model fields."""

        model = Game
        fields = ('id', 'board')


    def validate_board(self, value):
        """Ensure board is an nxn array of booleans."""
        try:
            board = json.loads(value)
        except Exception as e:
            raise serializers.ValidationError(str(e)) from e
        if not isinstance(board, list) or len(board) != Game.BOARD_SIZE:
            raise serializers.ValidationError(
                'Board must be a {0}x{0} array'.format(Game.BOARD_SIZE))
        for row in board:
            if not isinstance(row, list) or len(row) != Game.BOARD_SIZE:
                raise serializers.ValidationError(
                    'Board must be a {0}x{0} array'.format(Game.BOARD_SIZE))
            for val in row:
                if val is not None and not isinstance(val, bool):
                    raise serializers.ValidationError(
                        'Board can only contain boolean or nil values')
        return value
