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

    def test_create_game(self):
        """Test creation of a game."""
        old_count = Game.objects.count()
        self.game.save()
        new_count = Game.objects.count()
        self.assertNotEqual(old_count, new_count)


class ViewTestCase(TestCase):
    """Test the view."""

    def setUp(self):
        """Set up the tests."""
        data = {'board': [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]}
        self.response = APIClient().post(
            reverse('create'),
            data,
            format='json')

    def test_api_can_create_a_game(self):
        """Test game creation."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
