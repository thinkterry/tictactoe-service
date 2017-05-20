from django.test import TestCase
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
