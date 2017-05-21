import json
from django.db import models


class Game(models.Model):
    """Tic-tac-toe game."""

    BOARD_SIZE = 3

    board = models.CharField(max_length=255, blank=False)
    x_token = models.CharField(max_length=255, null=True)  # secret
    o_token = models.CharField(max_length=255, null=True)  # secret
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

    def _get_player(self, token):
        """Return the player the given token belongs to."""
        if token == self.x_token:
            return True
        elif token == self.o_token:
            return False
        else:
            raise ValueError('Unauthorized token: {}'.format(token))
