import json
import uuid
from unittest.mock import MagicMock
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Game

# @assume Game.BOARD_SIZE == 3 for simplicity in defining expected output


class ModelTestCase(TestCase):
    """Test the model."""

    def setUp(self):
        """Set up the tests."""
        self.game = Game()

    def test_model_can_create_a_game(self):
        """Test that the model can create a game."""
        old_count = Game.objects.count()
        self.game.save()
        new_count = Game.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_find_the_winner(self):
        """Test that the model can find the winner."""
        self.assertEqual(self.game._and_the_winner_is([
            [True, None, None],
            [None, True, None],
            [None, None, True]
        ]), True)
        self.assertEqual(self.game._and_the_winner_is([
            [False, None, None],
            [None, False, None],
            [None, None, False]
        ]), False)
        self.assertEqual(self.game._and_the_winner_is([
            [True, False, True],
            [None, False, False],
            [True, None, True]
        ]), None)
        self.assertEqual(self.game._and_the_winner_is([
            [True, True, True],
            [True, True, True],
            [True, True, True]
        ]), True)
        self.assertEqual(self.game._and_the_winner_is([
            [True, True, True],
            [None, None, None],
            [None, None, None]
        ]), True)
        self.assertEqual(self.game._and_the_winner_is([
            [None, None, False],
            [None, None, False],
            [None, None, False]
        ]), False)
        self.assertEqual(self.game._and_the_winner_is([
            [False, None, None],
            [False, None, None],
            [False, None, None]
        ]), False)


class ViewTestCase(TestCase):
    """Test the view."""

    def setUp(self):
        """Set up the tests."""
        self.client = APIClient()
        self.response = self.client.post(
            reverse('create'),
            format='json')
        self.game = Game.objects.all().first()
        self.fake_token_prefix = 'abc-123'
        self.x = 'x'
        self.o = 'o'

    def _join(self, player):
        fake_token = self.fake_token_prefix + player
        uuid.uuid4 = MagicMock(return_value=fake_token)
        response = self.client.post(
            reverse(
                'join',
                kwargs={'pk': self.game.id, 'player': player}),
            format='json')
        return response

    def test_api_can_get_a_game(self):
        """Test that the API can get a game."""
        response = self.client.get(
            reverse('details', kwargs={'pk': self.game.id}),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, self.game.board)

    def test_api_can_join_as_both_players(self):
        """Test that the API can join as both_players."""
        for player in [self.x, self.o]:
            fake_token = self.fake_token_prefix + player
            response = self._join(player)

            uuid.uuid4.assert_called_once()
            self.assertEquals(response.status_code, status.HTTP_200_OK)
            self.assertContains(response, fake_token)

    def test_api_cannot_join_twice(self):
        """Test that the API cannot join twice."""
        for _ in range(2):
            response = self._join(self.x)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_move_with_a_valid_token(self):
        """Test that the API can move with a valid token."""
        expected_board = json.dumps([
            [True, None, None],
            [None, None, None],
            [None, None, None]
        ])
        self._join(self.x)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, expected_board)

    def test_api_cannot_move_without_a_valid_token(self):
        """Test that the API cannot move without a valid token."""
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json')

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='...missing...')

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ')

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_requires_row_parameter(self):
        """Test that the API requires the row parameter."""
        self._join(self.x)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_requires_col_parameter(self):
        """Test that the API requires the col parameter."""
        self._join(self.x)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_requires_row_and_col_in_range(self):
        """Test that the API requires row and col be in range."""
        invalids = [
            {'row': -1, 'col': 0},
            {'row': 0, 'col': -1},
            {'row': 3, 'col': 0},
            {'row': 0, 'col': 3},
            {'row': 'row', 'col': 'col'}
        ]
        self._join(self.x)
        for invalid in invalids:
            response = self.client.post(
                reverse('details', kwargs={'pk': self.game.id}),
                invalid,
                format='json',
                HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)

            self.assertEquals(
                response.status_code,
                status.HTTP_400_BAD_REQUEST)

    def test_api_players_place_their_own_pieces(self):
        """Test that API players place their own pieces."""
        expected_board = json.dumps([
            [True, None, None],
            [None, None, None],
            [None, None, False]
        ])
        self._join(self.x)
        self._join(self.o)
        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 2, 'col': 2},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.o)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, expected_board)

    def test_api_moves_cannot_overwrite_existing_moves(self):
        """Test that API moves cannot overwrite existing moves."""
        self._join(self.x)
        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_moves_alternate(self):
        """Test that API moves alternate."""
        expected_board = json.dumps([
            [True, None, None],
            [None, None, None],
            [False, None, True]
        ])
        self._join(self.x)
        self._join(self.o)

        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)
        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 2, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.o)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 1, 'col': 1},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.o)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 2, 'col': 2},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 2},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

        response = self.client.get(
            reverse('details', kwargs={'pk': self.game.id}),
            format='json')

        self.assertContains(response, expected_board)

    def test_api_marks_winner(self):
        """Test that the API marks the winner."""
        expected_midgame_board = json.dumps([
            [True, True, None],
            [True, False, None],
            [False, None, None]
        ])
        expected_endgame_board = json.dumps([
            [True, True, False],
            [True, False, None],
            [False, None, None]
        ])
        self._join(self.x)
        self._join(self.o)

        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)
        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 2, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.o)
        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 1, 'col': 0},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)
        self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 1, 'col': 1},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.o)
        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 1},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.x)

        self.assertContains(response, expected_midgame_board)
        self.assertContains(response, '"winner":null')

        response = self.client.post(
            reverse('details', kwargs={'pk': self.game.id}),
            {'row': 0, 'col': 2},
            format='json',
            HTTP_AUTHORIZATION='Token ' + self.fake_token_prefix + self.o)

        self.assertContains(response, expected_endgame_board)
        self.assertContains(response, '"winner":false')
