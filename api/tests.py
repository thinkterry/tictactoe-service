import json
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Game


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


class ViewTestCase(TestCase):
    """Test the view."""

    fixtures = ['tests.json']

    def setUp(self):
        """Set up the tests."""
        self.client = APIClient()
        self.response = self.client.post(
            reverse('create'),
            format='json')

    def test_api_can_get_a_game(self):
        """Test that the API can get a game."""
        game = Game.objects.get(pk=Game.MASTER_GAME_ID)
        response = self.client.get(
            reverse('details', kwargs={'pk': game.id}),
            format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, game.board)

    def test_api_can_make_a_move(self):
        """Test that the API can make a move."""
        game = Game.objects.get(pk=Game.MASTER_GAME_ID)
        expected_game = json.dumps([
            [True, None, None],
            [None, None, None],
            [None, None, None]
        ])
        response = self.client.post(
            reverse('details', kwargs={'pk': game.id}),
            {'row': 0, 'col': 0},
            format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, expected_game)

    def test_api_requires_row_parameter(self):
        """Test that the API requires the row parameter."""
        game = Game.objects.get(pk=Game.MASTER_GAME_ID)
        response = self.client.post(
            reverse('details', kwargs={'pk': game.id}),
            {'col': 0},
            format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_requires_col_parameter(self):
        """Test that the API requires the col parameter."""
        game = Game.objects.get(pk=Game.MASTER_GAME_ID)
        response = self.client.post(
            reverse('details', kwargs={'pk': game.id}),
            {'row': 0},
            format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_api_requires_row_and_col_in_range(self):
        """Test that the API requires row and col be in range."""
        game = Game.objects.get(pk=Game.MASTER_GAME_ID)
        invalids = [
            {'row': -1, 'col': 0},
            {'row': 0, 'col': -1},
            {'row': 3, 'col': 0},
            {'row': 0, 'col': 3},
            {'row': 'row', 'col': 'col'}
        ]
        for invalid in invalids:
            response = self.client.post(
                reverse('details', kwargs={'pk': game.id}),
                invalid,
                format='json')
            self.assertEquals(
                response.status_code,
                status.HTTP_400_BAD_REQUEST)
