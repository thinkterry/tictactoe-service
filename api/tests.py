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

    def setUp(self):
        """Set up the tests."""
        self.client = APIClient()
        data = {'board': [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]}
        self.response = self.client.post(
            reverse('create'),
            data,
            format='json')

    def test_api_can_create_a_game(self):
        """Test that the API can create a game."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_get_a_game(self):
        """Test that the API can get a game."""
        game = Game.objects.get()
        response = self.client.get(
            reverse('details', kwargs={'pk': game.id}),
            format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, game)

    def test_api_can_update_a_game(self):
        """Test that the API can update a game."""
        game = Game.objects.get()
        new_data = {'board': [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]}
        res = self.client.put(
            reverse('details', kwargs={'pk': game.id}),
            new_data,
            format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_api_can_delete_a_game(self):
        """Test that the API can delete a game."""
        game = Game.objects.get()
        response = self.client.delete(
            reverse('details', kwargs={'pk': game.id}),
            format='json',
            follow=True)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
