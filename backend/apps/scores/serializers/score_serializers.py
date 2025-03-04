from rest_framework import serializers
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from ..models import Score, ScoreDetail
from users.serializers import UserSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'game': '3fa85f64-5717-4562-b3fc-2c963f66afa7',
                'game_name': 'Football Match 1 - Group Stage',
                'team1': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                'team1_name': 'Eagles',
                'team2': '3fa85f64-5717-4562-b3fc-2c963f66afa9',
                'team2_name': 'Falcons',
                'status': 'completed',
                'final_score_team1': 3,
                'final_score_team2': 2,
                'winner': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                'winner_name': 'Eagles',
                'is_draw': False,
                'notes': 'Exciting match with last-minute goal',
                'scorekeeper': {
                    'id': '3fa85f64-5717-4562-b3fc-2c963f66afa1',
                    'full_name': 'John Smith'
                },
                'score_details': [
                    {
                        'id': '3fa85f64-5717-4562-b3fc-2c963f66afb1',
                        'team': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                        'team_name': 'Eagles',
                        'player': '3fa85f64-5717-4562-b3fc-2c963f66afb2',
                        'player_name': 'Michael Johnson',
                        'points': 1,
                        'time_occurred': '00:15:30',
                        'period': 'First Half'
                    }
                ]
            },
            response_only=True,
        )
    ]
)
class ScoreSerializer(serializers.ModelSerializer):
    """
    Serializer for the Score model with detailed information.
    """
    game_name = serializers.CharField(source='game.name', read_only=True)
    team1 = serializers.UUIDField(source='game.team1.id', read_only=True)
    team1_name = serializers.CharField(source='game.team1.name', read_only=True)
    team2 = serializers.UUIDField(source='game.team2.id', read_only=True)
    team2_name = serializers.CharField(source='game.team2.name', read_only=True)
    winner_name = serializers.CharField(source='winner.name', read_only=True, allow_null=True)
    scorekeeper = UserSerializer(read_only=True)
    score_details = serializers.SerializerMethodField()
    
    class Meta:
        model = Score
        fields = [
            'id', 'game', 'game_name', 'team1', 'team1_name', 'team2', 'team2_name',
            'status', 'final_score_team1', 'final_score_team2', 'winner', 'winner_name',
            'is_draw', 'notes', 'scorekeeper', 'created_at', 'updated_at', 'score_details'
        ]
        read_only_fields = ['id', 'game', 'winner', 'is_draw', 'created_at', 'updated_at']
    
    def get_score_details(self, obj):
        score_details = obj.score_details.all().order_by('time_occurred')
        return ScoreDetailSerializer(score_details, many=True).data


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Update Example',
            value={
                'status': 'in_progress',
                'final_score_team1': 2,
                'final_score_team2': 1,
                'notes': 'Updated score as the game progresses'
            },
            request_only=True,
        )
    ]
)
class ScoreUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating a score.
    Only scorekeepers or admins can update scores.
    """
    class Meta:
        model = Score
        fields = ['status', 'final_score_team1', 'final_score_team2', 'notes']
    
    def update(self, instance, validated_data):
        # Update status if provided
        if 'status' in validated_data:
            new_status = validated_data['status']
            # Validate status transitions
            valid_transitions = {
                'pending': ['in_progress', 'cancelled'],
                'in_progress': ['completed', 'cancelled'],
                'completed': [],
                'cancelled': []
            }
            
            if new_status not in valid_transitions.get(instance.status, []):
                raise serializers.ValidationError({
                    'status': _('Invalid status transition from {} to {}'.format(
                        instance.get_status_display(), 
                        dict(Score.STATUS_CHOICES).get(new_status)
                    ))
                })
                
            # If status is changing to completed, ensure scores are provided
            if new_status == 'completed':
                if (instance.final_score_team1 is None or instance.final_score_team2 is None) and \
                   ('final_score_team1' not in validated_data or 'final_score_team2' not in validated_data):
                    raise serializers.ValidationError({
                        'status': _('Cannot complete a game without final scores for both teams')
                    })
        
        # Update instance with validated data
        instance = super().update(instance, validated_data)
        
        # If status is completed, determine the winner
        if instance.status == 'completed':
            winner = instance.determine_winner()
            if winner:
                instance.winner = winner
                instance.is_draw = False
            else:
                instance.winner = None
                instance.is_draw = True
            instance.save()
        
        return instance


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Verification Example',
            value={
                'verified': True,
                'notes': 'Verified after checking with both team captains'
            },
            request_only=True,
        )
    ]
)
class ScoreVerificationSerializer(serializers.Serializer):
    """
    Serializer for verifying a score by an administrator.
    """
    verified = serializers.BooleanField(required=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        # Only allow verification if the score is in completed status
        score = self.instance
        if score.status != 'completed':
            raise serializers.ValidationError({
                'verified': _('Cannot verify a score that is not in completed status')
            })
        return attrs
    
    def update(self, instance, validated_data):
        if validated_data.get('verified'):
            instance.verified_by = self.context['request'].user
            instance.verified_at = timezone.now()
            if 'notes' in validated_data and validated_data['notes']:
                instance.notes = instance.notes + '\nVerification: ' + validated_data['notes']
        else:
            instance.verified_by = None
            instance.verified_at = None
            if 'notes' in validated_data and validated_data['notes']:
                instance.notes = instance.notes + '\nVerification rejected: ' + validated_data['notes']
        
        instance.save()
        return instance


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Detail Example',
            value={
                'id': '3fa85f64-5717-4562-b3fc-2c963f66afb1',
                'score': '3fa85f64-5717-4562-b3fc-2c963f66afa6',
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                'team_name': 'Eagles',
                'player': '3fa85f64-5717-4562-b3fc-2c963f66afb2',
                'player_name': 'Michael Johnson',
                'points': 1,
                'time_occurred': '00:15:30',
                'period': 'First Half',
                'description': 'Goal from left wing'
            },
            response_only=True,
        )
    ]
)
class ScoreDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for the ScoreDetail model.
    """
    team_name = serializers.CharField(source='team.name', read_only=True)
    player_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ScoreDetail
        fields = [
            'id', 'score', 'team', 'team_name', 'player', 'player_name',
            'points', 'time_occurred', 'period', 'description'
        ]
        read_only_fields = ['id']
    
    def get_player_name(self, obj):
        if obj.player:
            return f"{obj.player.first_name} {obj.player.last_name}"
        return None


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Detail Create Example',
            value={
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                'player': '3fa85f64-5717-4562-b3fc-2c963f66afb2',
                'points': 1,
                'time_occurred': '00:15:30',
                'period': 'First Half',
                'description': 'Goal from left wing'
            },
            request_only=True,
        )
    ]
)
class ScoreDetailCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new score detail.
    """
    class Meta:
        model = ScoreDetail
        fields = [
            'team', 'player', 'points', 'time_occurred', 'period', 'description'
        ]
    
    def validate_team(self, value):
        # Ensure team is part of the game
        score = self.context.get('score')
        if score and value not in [score.game.team1, score.game.team2]:
            raise serializers.ValidationError(
                _('This team is not participating in the game.')
            )
        return value
    
    def validate_player(self, value):
        # Ensure player belongs to the selected team
        team = self.initial_data.get('team')
        if team and value and value.team.id != team:
            raise serializers.ValidationError(
                _('This player does not belong to the selected team.')
            )
        return value
    
    def create(self, validated_data):
        # Set the score and created_by fields
        score = self.context.get('score')
        user = self.context.get('request').user
        
        score_detail = ScoreDetail.objects.create(
            score=score,
            created_by=user,
            **validated_data
        )
        
        # Update the overall score
        if validated_data['team'] == score.game.team1:
            points = score.final_score_team1 or 0
            score.final_score_team1 = points + validated_data['points']
        else:
            points = score.final_score_team2 or 0
            score.final_score_team2 = points + validated_data['points']
            
        score.save(update_fields=['final_score_team1', 'final_score_team2', 'updated_at'])
        
        return score_detail