import json
from django.db import models


class Game(models.Model):
    """Tic-tac-toe game."""

    # JSON field per:
    # - http://stackoverflow.com/a/22343962
    # - https://www.stavros.io/posts/how-replace-django-model-field-property/
    _board = models.CharField(max_length=255, blank=False)

    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation."""
        board = ''
        for row in self.board:
            board += ' '.join(map(self._player_to_str, row)) + '\n'
        return board

    @property
    def board(self):
        """Get board as JSON object."""
        if self._board:
            return json.loads(self._board)
        else:
            return ''

    @board.setter
    def set_board(self, board):
        """Set board from JSON object."""
        self._board = json.dumps(board)

    def _player_to_str(self, player):
        if player is None:
            return '-'
        elif player:
            return 'X'
        else:
            return 'O'
