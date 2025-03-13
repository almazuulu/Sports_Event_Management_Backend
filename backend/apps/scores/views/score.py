from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse

from scores.models import Score
from scores.serializers import (
    ScoreSerializer, 
    ScoreUpdateSerializer,
    ScoreVerificationSerializer,
    ScoreCreateSerializer,
    PublicScoreSerializer,
    PublicLiveScoreSerializer,
    LeaderboardScoreSerializer
)
from scores.permissions import (
    IsScorekeeper,
    IsAssignedScorekeeper,
    CanManageScores,
    CanVerifyScores
)


class ScoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing game scores.
    
    Provides CRUD operations with appropriate permissions:
    - Admins can view, create, update, and verify scores
    - Scorekeepers can update scores for games they are assigned to
    - Public users can view basic score information
    
    Authentication is done via JWT Bearer token.
    """
    queryset = Score.objects.all()
    authentication_classes = [JWTAuthentication]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['game', 'status', 'verification_status']
    ordering_fields = ['created_at', 'updated_at', 'game__start_datetime']
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ScoreCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return ScoreUpdateSerializer
        elif self.action == 'verify_score':
            return ScoreVerificationSerializer
        return ScoreSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAuthenticated, CanManageScores]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [IsAuthenticated, IsAssignedScorekeeper|CanManageScores]
        elif self.action == 'verify_score':
            permission_classes = [IsAuthenticated, CanVerifyScores]
        elif self.action in ['public_scores', 'live_scores']:
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    
    def perform_create(self, serializer):
        """
        Set scorekeeper to the current user if not specified
        """
        if not serializer.validated_data.get('scorekeeper'):
            serializer.save(scorekeeper=self.request.user)
        else:
            serializer.save()
    
    @extend_schema(
        summary="List all scores",
        description="Retrieve a list of all game scores with filtering options",
        parameters=[
            OpenApiParameter(name="game", description="Filter by game ID", required=False, type=str),
            OpenApiParameter(name="status", description="Filter by score status", required=False, type=str),
            OpenApiParameter(name="verification_status", description="Filter by verification status", required=False, type=str),
            OpenApiParameter(name="ordering", description="Order by field (e.g., created_at, -created_at)", required=False, type=str)
        ],
        responses={200: ScoreSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        """
        List all scores.
        Supports filtering by game, status, and verification_status.
        """
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        summary="Create a score record",
        description="Initialize a score record for a game",
        request=ScoreCreateSerializer,
        responses={
            201: ScoreSerializer,
            400: OpenApiResponse(description="Bad request - invalid data")
        }
    )
    def create(self, request, *args, **kwargs):
        """
        Create a new score record for a game.
        Only users with score management permissions can create scores.
        """
        return super().create(request, *args, **kwargs)
    
    @extend_schema(
        summary="Retrieve score",
        description="Get detailed information about a specific score",
        responses={
            200: ScoreSerializer,
            404: OpenApiResponse(description="Not found - score does not exist")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information about a specific score.
        Includes score details and team information.
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Update score",
        description="Update details of a score (full update)",
        request=ScoreUpdateSerializer,
        responses={
            200: ScoreSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Not found - score does not exist")
        }
    )
    def update(self, request, *args, **kwargs):
        """
        Update all details of an existing score (full update).
        Only assigned scorekeepers or users with score management permissions can update scores.
        """
        return super().update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Partially update score",
        description="Update specific fields of a score",
        request=ScoreUpdateSerializer,
        responses={
            200: ScoreSerializer,
            400: OpenApiResponse(description="Bad request - invalid data"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Not found - score does not exist")
        }
    )
    def partial_update(self, request, *args, **kwargs):
        """
        Update specific fields of an existing score (partial update).
        Only assigned scorekeepers or users with score management permissions can update scores.
        """
        return super().partial_update(request, *args, **kwargs)
    
    @extend_schema(
        summary="Delete score",
        description="Remove a score record from the system",
        responses={
            204: OpenApiResponse(description="No content - score successfully deleted"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Not found - score does not exist")
        }
    )
    def destroy(self, request, *args, **kwargs):
        """
        Delete a score from the system.
        Only users with score management permissions can delete scores.
        """
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary="Verify score",
        description="Verify a completed score by an administrator",
        request=ScoreVerificationSerializer,
        responses={
            200: ScoreSerializer,
            400: OpenApiResponse(description="Bad request - invalid data or score not in completed status"),
            403: OpenApiResponse(description="Forbidden - insufficient permissions"),
            404: OpenApiResponse(description="Not found - score does not exist")
        }
    )
    @action(detail=True, methods=['patch'], url_path='verify')
    def verify_score(self, request, pk=None):
        """
        Verify a completed score.
        Sets the verification status and records the admin who verified the score.
        Only users with score verification permissions can verify scores.
        """
        score = self.get_object()
        serializer = self.get_serializer(score, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        # Return updated score
        return_serializer = ScoreSerializer(score)
        return Response(return_serializer.data)
    
    @extend_schema(
        summary="Public scores",
        description="Get a list of scores for public display",
        parameters=[
            OpenApiParameter(name="sport_event", description="Filter by sport event ID", required=False, type=str),
            OpenApiParameter(name="team", description="Filter by team ID", required=False, type=str),
            OpenApiParameter(name="status", description="Filter by status (e.g., completed)", required=False, type=str)
        ],
        responses={200: PublicScoreSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='public', permission_classes=[AllowAny])
    @method_decorator(cache_page(60*5))  # Cache for 5 minutes
    def public_scores(self, request):
        """
        Get a list of scores for public display.
        Includes limited information for completed or in-progress games.
        Supports filtering by sport event and team.
        """
        # Filter only completed or in-progress games
        queryset = self.queryset.filter(
            Q(status='completed') | Q(status='in_progress')
        )
        
        sport_event = request.query_params.get('sport_event')
        if sport_event:
            queryset = queryset.filter(game__sport_event=sport_event)
        
        team = request.query_params.get('team')
        if team:
            queryset = queryset.filter(
                Q(game__game_teams__team=team)
            )
        
        status_param = request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PublicScoreSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PublicScoreSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Live scores",
        description="Get a list of currently active game scores with live updates",
        parameters=[
            OpenApiParameter(name="sport_event", description="Filter by sport event ID", required=False, type=str)
        ],
        responses={200: PublicLiveScoreSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='live', permission_classes=[AllowAny])
    def live_scores(self, request):
        """
        Get a list of live game scores.
        Only includes games with 'in_progress' status.
        Includes current score and recent scoring events.
        """
        # Filter only in-progress games
        queryset = self.queryset.filter(status='in_progress')
        
        sport_event = request.query_params.get('sport_event')
        if sport_event:
            queryset = queryset.filter(game__sport_event=sport_event)
        
        serializer = PublicLiveScoreSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Scorekeeper's assigned games",
        description="Get scores for games assigned to the current scorekeeper",
        responses={200: ScoreSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='my-assignments', permission_classes=[IsAuthenticated, IsScorekeeper])
    def my_assignments(self, request):
        """
        Get scores for games assigned to the current scorekeeper.
        Only available to users with the scorekeeper role.
        """
        queryset = self.queryset.filter(scorekeeper=request.user)
        
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Event leaderboard",
        description="Get a leaderboard for a specific sport event",
        parameters=[
            OpenApiParameter(name="sport_event", description="Sport event ID", required=True, type=str)
        ],
        responses={200: LeaderboardScoreSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='leaderboard', permission_classes=[AllowAny])
    @method_decorator(cache_page(60*15))  # Cache for 15 minutes
    def event_leaderboard(self, request):
        """
        Get a leaderboard for a specific sport event.
        Calculates team standings based on game results.
        """
        sport_event = request.query_params.get('sport_event')
        if not sport_event:
            return Response(
                {"error": "sport_event parameter is required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all completed games for this sport event
        scores = Score.objects.filter(
            game__sport_event=sport_event,
            status='completed',
            verification_status='verified'
        )
        
        # Get all teams that participated in these games
        team_ids = set()
        for score in scores:
            for team_relation in score.game.game_teams.all():
                team_ids.add(team_relation.team.id)
        
        # Initialize leaderboard data
        leaderboard = []
        for team_id in team_ids:
            team = scores[0].game.game_teams.filter(team_id=team_id).first().team
            
            # Calculate team statistics
            team_stats = {
                'team_id': team_id,
                'team_name': team.name,
                'played': 0,
                'won': 0,
                'drawn': 0,
                'lost': 0,
                'goals_for': 0,
                'goals_against': 0,
                'goal_difference': 0,
                'points': 0
            }
            
            # Process each score to update statistics
            for score in scores:
                # Check if this team participated in this game
                team_designations = score.game.game_teams.filter(team_id=team_id)
                if not team_designations.exists():
                    continue
                
                # Increment games played
                team_stats['played'] += 1
                
                # Get team designation
                team_designation = team_designations.first().designation
                
                # Set team position (1 or 2) based on designation
                team_position = 1 if team_designation in ['team_a', 'home'] else 2
                
                # Get opponent position
                opponent_position = 2 if team_position == 1 else 1
                
                # Add goals for/against
                if team_position == 1:
                    team_stats['goals_for'] += score.goals_for_team1
                    team_stats['goals_against'] += score.goals_against_team1
                else:
                    team_stats['goals_for'] += score.goals_for_team2
                    team_stats['goals_against'] += score.goals_against_team2
                
                # Determine win/loss/draw
                if score.is_draw:
                    team_stats['drawn'] += 1
                    team_stats['points'] += 1  # 1 point for a draw
                elif score.winner and score.winner.id == team_id:
                    team_stats['won'] += 1
                    team_stats['points'] += 3  # 3 points for a win
                else:
                    team_stats['lost'] += 1
                    # 0 points for a loss
            
            # Calculate goal difference
            team_stats['goal_difference'] = team_stats['goals_for'] - team_stats['goals_against']
            
            leaderboard.append(team_stats)
        
        # Sort leaderboard by points (descending), goal difference, goals for
        leaderboard.sort(
            key=lambda x: (-x['points'], -x['goal_difference'], -x['goals_for'])
        )
        
        return Response(leaderboard)


