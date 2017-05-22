import json
from rest_framework import serializers
from .models import Game


class GameSerializer(serializers.ModelSerializer):
    """Serialize a game."""

    class Meta:
        """Map serializer fields to model fields."""

        model = Game
        fields = (
            'id',
            'board',
            'x_token',
            'o_token',
            'current_player',
            'winner')
        # Ideally these secret tokens would be 'write_only' to
        # ensure they remain secret to the users. Unfortunately,
        # doing so also ensures they remain secret to the views
        # trying to use them to authorize requests.
        # 'write_only' per http://stackoverflow.com/a/36771366:
        # extra_kwargs = {
        #     'x_token': {'write_only': True},
        #     'o_token': {'write_only': True}}


    def validate_board(self, value):
        """Ensure board is an NxN array of booleans."""
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

    def validate_move(self, game, board, player, row, col):
        """Ensure moves cannot overwrite existing moves."""
        if board[row][col] is not None:
            raise serializers.ValidationError(
                'Moves cannot overwrite existing moves')
        if player != game.current_player:
            raise serializers.ValidationError(
                'Not your turn')
