from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _
from django.db.models import Q, F
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from .models import Leaderboard, LeaderboardEntry
from .serializers import (
    LeaderboardSerializer,
    LeaderboardSummarySerializer, 
    LeaderboardEntrySerializer,
    TeamLeaderboardSerializer
)
from .permissions import CanManageLeaderboards
from users.permissions import IsAdminUser


class LeaderboardViewSet(viewsets.ModelViewSet):
    """
    API endpoint for leaderboards.
    Provides read operations for all users and write operations for admins.
    """
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['sport_event', 'is_final']
    search_fields = ['sport_event__name']
    ordering_fields = ['sport_event__name', 'last_updated']
    
    def get_queryset(self):
        """
        Return all leaderboards.
        """
        return Leaderboard.objects.all().select_related('sport_event')
    
    def get_serializer_class(self):
        if self.action == 'list':
            return LeaderboardSummarySerializer
        return LeaderboardSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy', 'calculate', 'finalize']:
            permission_classes = [IsAuthenticated, IsAdminUser]
        else:
            permission_classes = [AllowAny]
        return [permission() for permission in permission_classes]
    
    @extend_schema(
        summary="List leaderboards",
        description="Get a list of all leaderboards with basic information",
        parameters=[
            OpenApiParameter(name="sport_event", description="Filter by sport event ID", required=False, type=str),
            OpenApiParameter(name="is_final", description="Filter by final status", required=False, type=bool),
            OpenApiParameter(name="search", description="Search by sport event name", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order results (e.g., last_updated, -last_updated)", required=False, type=str)
        ],
        responses={200: LeaderboardSummarySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all leaderboards.
        
        Returns a paginated list of leaderboards with basic information.
        Supports filtering by sport event and final status.
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve leaderboard",
        description="Get detailed information about a specific leaderboard including all team entries",
        responses={
            200: LeaderboardSerializer,
            404: OpenApiResponse(description="Leaderboard not found")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific leaderboard.
        
        Returns detailed leaderboard information including all team entries
        sorted by position.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create leaderboard",
        description="Initialize a new leaderboard for a sport event. Admin only.",
        request=LeaderboardSerializer,
        responses={
            201: LeaderboardSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            403: OpenApiResponse(description="Forbidden - admin access required")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new leaderboard.
        
        Initializes a new leaderboard for a sport event.
        Only administrators can create leaderboards.
        """
        # Make sure we have a sport_event
        if 'sport_event' not in request.data:
            return Response(
                {"sport_event": "This field is required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    @extend_schema(
        summary="Update leaderboard",
        description="Update a leaderboard. Admin only.",
        request=LeaderboardSerializer,
        responses={
            200: LeaderboardSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            403: OpenApiResponse(description="Forbidden - admin access required"),
            404: OpenApiResponse(description="Not found - leaderboard does not exist")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update a leaderboard.
        
        Updates leaderboard properties (not entries).
        Only administrators can update leaderboards.
        """
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete leaderboard",
        description="Delete a leaderboard. Admin only.",
        responses={
            204: OpenApiResponse(description="No content - leaderboard successfully deleted"),
            403: OpenApiResponse(description="Forbidden - admin access required"),
            404: OpenApiResponse(description="Not found - leaderboard does not exist")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a leaderboard.
        
        Permanently removes the leaderboard and all its entries.
        Only administrators can delete leaderboards.
        """
        return super().destroy(request, *args, **kwargs)
    
    @action(detail=True, methods=['post'], url_path='calculate')
    @extend_schema(
        summary="Calculate leaderboard",
        description="Recalculate the leaderboard based on current game results. Admin only.",
        responses={
            200: LeaderboardSerializer,
            403: OpenApiResponse(description="Forbidden - admin access required"),
            404: OpenApiResponse(description="Not found - leaderboard does not exist")
        }
    )
    def calculate(self, request, pk=None):
        """
        Calculate/recalculate a leaderboard.
        
        Updates all entries based on current game results.
        Only administrators can trigger leaderboard calculations.
        """
        leaderboard = self.get_object()
        
        # Get the sport event
        sport_event = leaderboard.sport_event
        
        # Get all completed and verified games for this sport event
        from scores.models import Score
        from games.models import Game
        
        games = Game.objects.filter(
            sport_event=sport_event,
            status='completed',
            score__verification_status='verified'
        ).select_related('score')
        
        # Get all teams that participated in these games
        team_ids = set()
        for game in games:
            for game_team in game.game_teams.all():
                team_ids.add(game_team.team_id)
        
        # Calculate stats for each team
        entries = []
        for team_id in team_ids:
            # Get team object
            from teams.models import Team
            team = Team.objects.get(id=team_id)
            
            # Calculate team statistics
            stats = {
                'team': team,
                'played': 0,
                'won': 0,
                'drawn': 0,
                'lost': 0,
                'goals_for': 0,
                'goals_against': 0,
                'goal_difference': 0,
                'points': 0,
                'clean_sheets': 0,
                'yellow_cards': 0,
                'red_cards': 0
            }
            
            # Process each game
            for game in games:
                # Check if this team participated in this game
                team_designations = game.game_teams.filter(team_id=team_id)
                if not team_designations.exists():
                    continue
                
                # Increment games played
                stats['played'] += 1
                
                # Get the score
                score = game.score
                
                # Get team designation
                team_designation = team_designations.first().designation
                
                # Set team position (1 or 2) based on designation
                team_position = 1 if team_designation in ['team_a', 'home'] else 2
                other_position = 2 if team_position == 1 else 1
                
                # Get goals for/against
                if team_position == 1:
                    goals_for = score.final_score_team1 or 0
                    goals_against = score.final_score_team2 or 0
                else:
                    goals_for = score.final_score_team2 or 0
                    goals_against = score.final_score_team1 or 0
                
                stats['goals_for'] += goals_for
                stats['goals_against'] += goals_against
                
                # Check for clean sheet
                if goals_against == 0:
                    stats['clean_sheets'] += 1
                
                # Determine win/loss/draw and points
                if score.is_draw:
                    stats['drawn'] += 1
                    stats['points'] += 1  # 1 point for a draw
                elif score.winner and score.winner.id == team_id:
                    stats['won'] += 1
                    stats['points'] += 3  # 3 points for a win
                else:
                    stats['lost'] += 1  # 0 points for a loss
                
                # Get yellow/red cards from score details
                # This is just a placeholder; implementation depends on how cards are tracked
                if hasattr(score, 'score_details'):
                    yellow_cards = score.score_details.filter(
                        team_id=team_id, 
                        event_type='yellow_card'
                    ).count()
                    
                    red_cards = score.score_details.filter(
                        team_id=team_id, 
                        event_type='red_card'
                    ).count()
                    
                    stats['yellow_cards'] += yellow_cards
                    stats['red_cards'] += red_cards
            
            # Calculate goal difference
            stats['goal_difference'] = stats['goals_for'] - stats['goals_against']
            
            # Update or create leaderboard entry
            entry, created = LeaderboardEntry.objects.update_or_create(
                leaderboard=leaderboard,
                team=team,
                defaults={
                    'played': stats['played'],
                    'won': stats['won'],
                    'drawn': stats['drawn'],
                    'lost': stats['lost'],
                    'goals_for': stats['goals_for'],
                    'goals_against': stats['goals_against'],
                    'goal_difference': stats['goal_difference'],
                    'points': stats['points'],
                    'clean_sheets': stats['clean_sheets'],
                    'yellow_cards': stats['yellow_cards'],
                    'red_cards': stats['red_cards'],
                    'position': 0  # Temporary position, will be updated below
                }
            )
            entries.append(entry)
        
        # Sort entries by points, goal difference, goals for
        sorted_entries = sorted(
            entries,
            key=lambda x: (-x.points, -x.goal_difference, -x.goals_for)
        )
        
        # Update positions
        for i, entry in enumerate(sorted_entries):
            entry.position = i + 1
            entry.save(update_fields=['position'])
        
        # Update the leaderboard's last_updated timestamp
        leaderboard.save()
        
        # Return the updated leaderboard
        serializer = self.get_serializer(leaderboard)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], url_path='finalize')
    @extend_schema(
        summary="Finalize leaderboard",
        description="Mark a leaderboard as final. Admin only.",
        responses={
            200: LeaderboardSerializer,
            403: OpenApiResponse(description="Forbidden - admin access required"),
            404: OpenApiResponse(description="Not found - leaderboard does not exist")
        }
    )
    def finalize(self, request, pk=None):
        """
        Finalize a leaderboard.
        
        Marks the leaderboard as final, indicating the tournament is complete.
        Only administrators can finalize leaderboards.
        """
        leaderboard = self.get_object()
        leaderboard.is_final = True
        leaderboard.save(update_fields=['is_final'])
        
        serializer = self.get_serializer(leaderboard)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='team/(?P<team_id>[^/.]+)')
    @extend_schema(
        summary="Team leaderboards",
        description="Get all leaderboard entries for a specific team across different sport events",
        parameters=[
            OpenApiParameter(name="team_id", location=OpenApiParameter.PATH, description="Team ID", required=True, type=str)
        ],
        responses={200: TeamLeaderboardSerializer(many=True)}
    )
    def team_leaderboards(self, request, team_id=None):
        """
        Get all leaderboard entries for a specific team.
        
        Returns a team's standings across multiple sport events.
        """
        # Get all leaderboard entries for the team
        entries = LeaderboardEntry.objects.filter(
            team_id=team_id
        ).select_related('leaderboard', 'leaderboard__sport_event', 'team')
        
        # Format the response with sport event information
        results = []
        for entry in entries:
            results.append({
                'sport_event_id': str(entry.leaderboard.sport_event.id),
                'sport_event_name': entry.leaderboard.sport_event.name,
                'position': entry.position,
                'played': entry.played,
                'won': entry.won,
                'drawn': entry.drawn,
                'lost': entry.lost,
                'points': entry.points,
                'goals_for': entry.goals_for,
                'goals_against': entry.goals_against,
                'goal_difference': entry.goal_difference,
                'is_final': entry.leaderboard.is_final
            })
        
        serializer = TeamLeaderboardSerializer(results, many=True)
        return Response(serializer.data)


class LeaderboardEntryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for leaderboard entries.
    Read-only viewset - entries are calculated and updated through the leaderboard.
    """
    queryset = LeaderboardEntry.objects.all()
    serializer_class = LeaderboardEntrySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['leaderboard', 'team', 'position']
    ordering_fields = ['position', 'points', 'goal_difference', 'played']
    
    @extend_schema(
        summary="List leaderboard entries",
        description="Get a list of leaderboard entries with filtering options",
        parameters=[
            OpenApiParameter(name="leaderboard", description="Filter by leaderboard ID", required=False, type=str),
            OpenApiParameter(name="team", description="Filter by team ID", required=False, type=str),
            OpenApiParameter(name="position", description="Filter by position", required=False, type=int),
            OpenApiParameter(name="ordering", description="Order results (e.g., position, -points)", required=False, type=str)
        ],
        responses={200: LeaderboardEntrySerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List leaderboard entries.
        
        Returns a paginated list of leaderboard entries.
        Supports filtering by leaderboard, team, and position.
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve leaderboard entry",
        description="Get detailed information about a specific leaderboard entry",
        responses={
            200: LeaderboardEntrySerializer,
            404: OpenApiResponse(description="Leaderboard entry not found")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a specific leaderboard entry.
        
        Returns detailed information about a team's standing in a leaderboard.
        """
        return super().retrieve(request, *args, **kwargs)