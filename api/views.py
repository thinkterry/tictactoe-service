import json
from rest_framework import generics
from .serializers import GameSerializer
from .models import Game


class CreateView(generics.ListCreateAPIView):
    """Handle POST."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        """Save new object to database."""
        empty_board = json.dumps([
            [None, None, None],
            [None, None, None],
            [None, None, None]])
        serializer.save(_board=empty_board)


class DetailsView(generics.RetrieveUpdateDestroyAPIView):
    """Handle GET, PUT, and DELETE."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer
