import json
from django.db import models


class Game(models.Model):
    """Tic-tac-toe game.

    Each player, upon joining the game as their chosen piece (X or O)
    is given a "secret" token, which authorizes them to make moves.
    Internally, the X-player is represented by True and the O-player
    by False."""

    BOARD_SIZE = 3

    board = models.CharField(max_length=255, blank=False, default=json.dumps(
        [[None] * BOARD_SIZE] * BOARD_SIZE))
    current_player = models.BooleanField(default=True)
    winner = models.NullBooleanField()
    x_token = models.CharField(max_length=255, null=True)
    o_token = models.CharField(max_length=255, null=True)
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
        """Return string representation."""
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

    def _and_the_winner_is(self, board):
        """Return the winner, if one yet exists."""
        if self.winner is not None:
            return self.winner

        row_winner = self._row_winner(board)
        column_winner = self._column_winner(board)
        diagonal_ul_lr = self._diagonal_ul_lr(board)
        diagonal_ll_ur = self._diagonal_ll_ur(board)

        # verbosely check for None because False is a valid value
        if row_winner is not None:
            return row_winner
        if column_winner is not None:
            return column_winner
        if diagonal_ul_lr is not None:
            return diagonal_ul_lr
        if diagonal_ll_ur is not None:
            return diagonal_ll_ur
        return None

    def _row_winner(self, board):
        """Return the winner by row."""
        for r in range(len(board)):
            ref = board[r][0]
            if ref is None:
                continue
            if all([ref == val for val in board[r][1:]]):
                return ref
        return None

    def _column_winner(self, board):
        """Return the winner by column."""
        for c in range(len(board[0])):
            ref = board[0][c]
            if ref is None:
                continue
            all_match = True  # innocent until proven guilty
            for r in range(1, len(board)):
                if ref != board[r][c]:
                    all_match = False
                    break
            if all_match:
                return ref
        return None

    def _diagonal_ul_lr(self, board):
        """Return the winner by the upper-left to lower-right diagonal."""
        all_match = True  # innocent until proven guilty
        ref = board[0][0]
        for d in range(1, len(board)):
            if ref != board[d][d]:
                all_match = False
                break
        if all_match:
            return ref
        return None

    def _diagonal_ll_ur(self, board):
        """Return the winner by the lower-left to upper-right diagonal."""
        all_match = True  # innocent until proven guilty
        ref = board[-1][0]
        for d in range(1, len(board)):
            if ref != board[-1 - d][d]:
                all_match = False
                break
        if all_match:
            return ref
        return None
