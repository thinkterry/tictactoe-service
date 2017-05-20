from rest_framework import generics
from .serializers import GameSerializer
from .models import Game


class CreateView(generics.ListCreateAPIView):
    """The create view."""

    queryset = Game.objects.all()
    serializer_class = GameSerializer

    def perform_create(self, serializer):
        """Save new object to database."""
        serializer.save()
