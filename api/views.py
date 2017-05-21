import json
from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GameSerializer
from .models import Game



class GameList(generics.ListCreateAPIView):
    """Handle POST."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        """Save new object to database."""
        empty_board = json.dumps([
            [None, None, None],
            [None, None, None],
            [None, None, None]])
        serializer.save(board=empty_board)


class GameDetail(APIView):
    """Handle GET, POST, PUT, and DELETE."""

    def get(self, request, pk, format=None):
        """Get a game."""
        # per http://stackoverflow.com/a/4300377
        game = Game.objects.get(pk=Game.MASTER_GAME_ID)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """Make a move."""
        player = True  # @todo use authorization token
        row, col, err = self._parse_row_col()
        if err:
            return err

        # per http://stackoverflow.com/a/4300377
        game = Game.objects.get(pk=Game.MASTER_GAME_ID)

        board = json.loads(game.board)
        board[row][col] = player
        board_json = json.dumps(board)

        serializer = GameSerializer(data={'board': board_json})
        if not serializer.is_valid():
            raise serializers.ValidationError(
                'Invalid move at board[{}][{}]: {}'.format(
                    row, col, serializer.errors))
        serializer.update(game, serializer.data)
        return Response(serializer.data)

    def _parse_row_col(self):
        """Extract row and col from request body."""
        row = self.request.data.get('row')
        col = self.request.data.get('col')
        try:
            row = int(row)
            col = int(col)
        except Exception:
            return None, None, Response(
                'row and col required in request body',
                status=status.HTTP_400_BAD_REQUEST)
        if not 0 <= row < Game.BOARD_SIZE or not 0 <= col < Game.BOARD_SIZE:
            return None, None, Response(
                'row and col must be between {} and {}'.format(
                    0, Game.BOARD_SIZE - 1),
                status=status.HTTP_400_BAD_REQUEST)
        return row, col, None
