from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models import Score
from ..serializers import ScoreSerializer

class TeamScoreViewSet(viewsets.ViewSet):
    """
    A viewset for retrieving team scores and team-specific data.
    """

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def team_scores(self, request, team_id=None):
        """
        Retrieves all scores for a specific team. Admin users have full access, Team captains can only access their team, Public users see limited information 
        """
        # Check permissions: Admin users have full access, Team captains only access their team
        from apps.teams.models import Team
        team = Team.objects.get(id=team_id)
        if request.user.role == 'team_captain' and request.user.team != team:
            return Response({'detail': 'You do not have permission to view this team\'s scores.'}, status=403)
        
        scores = Score.objects.filter(team=team)
        serializer = ScoreSerializer(scores, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def team_scoreboard(self, request):
        """
        Provides a comprehensive view of team rankings based on game results.  Public access (no authentication required) 
        """
        from apps.teams.models import Team
        teams = Team.objects.all()
        team_rankings = []
        
        for team in teams:
            wins = Score.objects.filter(team=team, result='win').count()
            losses = Score.objects.filter(team=team, result='loss').count()
            total_points = Score.objects.filter(team=team).aggregate(total_points=Sum('points'))['total_points'] or 0
            team_rankings.append({
                'team': team.name,
                'wins': wins,
                'losses': losses,
                'total_points': total_points,
            })
        
        # Sort the teams by total points, then by wins
        team_rankings.sort(key=lambda x: (-x['total_points'], -x['wins']))
        
        return Response(team_rankings)
