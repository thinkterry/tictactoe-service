import json
from django.db import models


class Game(models.Model):
    """Tic-tac-toe game."""

    MASTER_GAME_ID = 1  # hard-code for minimum viable product
    BOARD_SIZE = 3

    board = models.CharField(max_length=255, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return string representation."""
        board = json.loads(self.board)
        retval = ''
        for row in board:
            retval += ' '.join(map(self._player_to_str, row)) + '\n'
        return retval

    def _player_to_str(self, player):
        if player is None:
            return '-'
        elif player:
            return 'X'
        else:
            return 'O'
