from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from games.models import Game
from games.serializers import GameSerializer
from games.permissions import CanViewGame, CanManageGame, CanUpdateGameStatus, CanManageGameTeams, CanManageGamePlayers


@extend_schema_view(
    list=extend_schema(description="List all games."),
    retrieve=extend_schema(description="Retrieve a specific game."),
    create=extend_schema(description="Create a new game."),
    update=extend_schema(description="Update an existing game."),
    partial_update=extend_schema(description="Partially update a game."),
    destroy=extend_schema(description="Delete a game."),
)
class GameViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing game instances.
    """
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [IsAuthenticated]  # Ensures the user is authenticated by default

    def get_permissions(self):
        """
        Return permissions based on action.
        """
        if self.action in ['list', 'retrieve']:
            return [CanViewGame()]
        elif self.action in ['create', 'update', 'destroy']:
            return [CanManageGame()]
        elif self.action == 'partial_update':
            return [CanUpdateGameStatus()]
        elif self.action == 'assign_teams':
            return [CanManageGameTeams()]
        elif self.action == 'assign_players':
            return [CanManageGamePlayers()]
        return super().get_permissions()

    def perform_create(self, serializer):
        """
        Custom perform create to set the 'created_by' field as the current user.
        """
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[CanManageGameTeams])
    @extend_schema(
        description="Assign teams to a game.",
        request=GameSerializer,
        responses={200: GameSerializer},
    )
    def assign_teams(self, request, pk=None):
        """
        Custom action to assign teams to a game. Only accessible to admins.
        """
        game = self.get_object()  # Get the game instance
        # Assume that the request contains team data (you can adjust this based on your needs)
        teams_data = request.data.get('teams', [])

        # You should define your logic for assigning teams here
        # For example, you might want to validate the teams and assign them to the game

        # For demonstration purposes, assuming teams_data is a list of team IDs
        # Update the game object to reflect the assigned teams
        game.teams.set(teams_data)  # Adjust if your model is set up differently
        game.save()

        # Return the updated game data
        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'], permission_classes=[CanManageGamePlayers])
    @extend_schema(
        description="Assign players to a game.",
        request=GameSerializer,
        responses={200: GameSerializer},
    )
    def assign_players(self, request, pk=None):
        """
        Custom action to assign players to a game. Only accessible to team captains.
        """
        game = self.get_object()  # Get the game instance
        players_data = request.data.get('players', [])

        # Implement logic for assigning players to a game, this could depend on your models
        # Example: game.players.set(players_data) if you have a players field on the game

        # For demonstration purposes, assuming players_data is a list of player IDs
        game.players.set(players_data)  # Adjust if your model is set up differently
        game.save()

        return Response(GameSerializer(game).data, status=status.HTTP_200_OK)
