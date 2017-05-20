from django.db import models
import json


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
        return self.board()

    @property
    def board(self):
        """Get board."""
        return json.loads(self._board)

    @board.setter
    def set_board(self, board):
        """Set board."""
        self._board = json.dumps(board)
