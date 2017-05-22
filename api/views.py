import json
import uuid
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import GameSerializer
from .models import Game
from .permissions import IsOwnerOrReadOnly



class GameList(generics.ListCreateAPIView):
    """List and create operations on games."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer


class GameDetail(APIView):
    """CRUD operations on a game."""

    permission_classes = (IsOwnerOrReadOnly,)

    def get(self, request, pk, format=None):
        """Get a game."""
        # per http://stackoverflow.com/a/4300377
        game = Game.objects.get(pk=pk)
        serializer = GameSerializer(game)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        """Make a move."""
        game = Game.objects.get(pk=pk)
        # per http://stackoverflow.com/a/22567895
        self.check_object_permissions(self.request, game)

        player = game._get_player(self._parse_header_token(self.request))
        row, col, err = self._parse_row_col()
        if err:
            return err
        board = json.loads(game.board)
        GameSerializer().validate_move(game, board, player, row, col)

        board[row][col] = player

        serializer = GameSerializer(data={
            'board': json.dumps(board),
            'current_player': (not game.current_player),
            'winner': game._and_the_winner_is(board)})
        serializer.is_valid(raise_exception=True)
        serializer.update(game, serializer.data)
        return Response(serializer.data)

    # @DRY permissions.py
    def _parse_header_token(self, request):
        """Extract authorization token from request headers."""
        try:
            # per http://stackoverflow.com/a/3889790
            return request.META.get(
                'HTTP_AUTHORIZATION'
            ).strip().split()[1]
        except Exception:
            return None

    def _parse_row_col(self):
        """Extract row and col from request body, if able.

        Returns:
        row, col, err Response
        """
        row = self.request.data.get('row')
        col = self.request.data.get('col')
        try:
            row = int(row)
            col = int(col)
        except Exception:
            return None, None, Response(
                'Row and col required in request body',
                status=status.HTTP_400_BAD_REQUEST)
        if not 0 <= row < Game.BOARD_SIZE or not 0 <= col < Game.BOARD_SIZE:
            return None, None, Response(
                'Row and col must be between {} and {}'.format(
                    0, Game.BOARD_SIZE - 1),
                status=status.HTTP_400_BAD_REQUEST)
        return row, col, None


class JoinGame(APIView):
    """Join a game."""

    def post(self, request, pk, player, format=None):
        """Join a game."""
        game = Game.objects.get(pk=pk)
        if game.x_token and game.o_token:
            return Response(
                'Both X and O have already joined this game',
                status=status.HTTP_403_FORBIDDEN)
        if player == 'X':
            if game.x_token:
                return Response(
                    'X has already joined this game; try joining as O',
                    status=status.HTTP_403_FORBIDDEN)
            else:
                return self._update_token(game, player)
        else:
            if game.o_token:
                return Response(
                    'O has already joined this game; try joining as X',
                    status=status.HTTP_403_FORBIDDEN)
            else:
                return self._update_token(game, player)

    def _update_token(self, game, player):
        """Generate an authorization token for either the X or O player."""
        token = str(uuid.uuid4())
        token_field_name = player.lower() + '_token'
        serializer = GameSerializer(data={
            'board': game.board,
            token_field_name: token})
        serializer.is_valid(raise_exception=True)
        serializer.update(game, serializer.data)
        return Response({'token': token})
