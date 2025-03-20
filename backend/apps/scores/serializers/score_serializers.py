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
                'goals_for_team1': 3,
                'goals_against_team1': 2,
                'goals_for_team2': 2,
                'goals_against_team2': 3,
                'goal_difference_team1': 1,
                'goal_difference_team2': -1,
                'winner': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                'winner_name': 'Eagles',
                'is_draw': False,
                'notes': 'Exciting match with last-minute goal',
                'verification_status': 'verified',
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
                        'minute': 15,
                        'period': 'First Half',
                        'event_type': 'goal'
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
    # Get team information from game_teams instead of direct game properties
    game_name = serializers.CharField(source='game.name', read_only=True)
    team1 = serializers.SerializerMethodField()
    team1_name = serializers.SerializerMethodField()
    team2 = serializers.SerializerMethodField()
    team2_name = serializers.SerializerMethodField()
    winner_name = serializers.CharField(source='winner.name', read_only=True, allow_null=True)
    scorekeeper = UserSerializer(read_only=True)
    score_details = serializers.SerializerMethodField()
    # Calculate goal differences
    goal_difference_team1 = serializers.SerializerMethodField()
    goal_difference_team2 = serializers.SerializerMethodField()
    
    class Meta:
        model = Score
        fields = [
            'id', 'game', 'game_name', 'team1', 'team1_name', 'team2', 'team2_name',
            'status', 'final_score_team1', 'final_score_team2', 
            'goals_for_team1', 'goals_against_team1', 'goal_difference_team1',
            'goals_for_team2', 'goals_against_team2', 'goal_difference_team2',
            'time_elapsed', 'winner', 'winner_name',
            'is_draw', 'notes', 'verification_status', 'scorekeeper', 
            'created_at', 'updated_at', 'score_details'
        ]
        read_only_fields = [
            'id', 'game', 'winner', 'is_draw', 'created_at', 'updated_at',
            'goal_difference_team1', 'goal_difference_team2'
        ]
    
    def get_team1(self, obj):
        # Get team1 from game_team with designation team_a or home
        team1_relation = obj.game.game_teams.filter(designation__in=['team_a', 'home']).first()
        if team1_relation:
            return str(team1_relation.team.id)
        return None
    
    def get_team1_name(self, obj):
        team1_relation = obj.game.game_teams.filter(designation__in=['team_a', 'home']).first()
        if team1_relation:
            return team1_relation.team.name
        return None
    
    def get_team2(self, obj):
        team2_relation = obj.game.game_teams.filter(designation__in=['team_b', 'away']).first()
        if team2_relation:
            return str(team2_relation.team.id)
        return None
    
    def get_team2_name(self, obj):
        team2_relation = obj.game.game_teams.filter(designation__in=['team_b', 'away']).first()
        if team2_relation:
            return team2_relation.team.name
        return None
    
    def get_score_details(self, obj):
        score_details = obj.score_details.all().order_by('time_occurred')
        return ScoreDetailSerializer(score_details, many=True).data
    
    def get_goal_difference_team1(self, obj):
        return obj.calculate_goal_difference(1)
    
    def get_goal_difference_team2(self, obj):
        return obj.calculate_goal_difference(2)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Update Example',
            value={
                'status': 'in_progress',
                'final_score_team1': 2,
                'final_score_team2': 1,
                'time_elapsed': '45+2',
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
        fields = [
            'status', 'final_score_team1', 'final_score_team2', 
            'goals_for_team1', 'goals_against_team1',
            'goals_for_team2', 'goals_against_team2',
            'time_elapsed', 'notes'
        ]
    
    def validate(self, attrs):
        # Ensure scores are not negative
        if 'final_score_team1' in attrs and attrs['final_score_team1'] < 0:
            raise serializers.ValidationError({'final_score_team1': _('Score cannot be negative')})
        
        if 'final_score_team2' in attrs and attrs['final_score_team2'] < 0:
            raise serializers.ValidationError({'final_score_team2': _('Score cannot be negative')})
        
        # Ensure goals for/against are not negative
        if 'goals_for_team1' in attrs and attrs['goals_for_team1'] < 0:
            raise serializers.ValidationError({'goals_for_team1': _('Goals cannot be negative')})
        
        if 'goals_against_team1' in attrs and attrs['goals_against_team1'] < 0:
            raise serializers.ValidationError({'goals_against_team1': _('Goals cannot be negative')})
        
        if 'goals_for_team2' in attrs and attrs['goals_for_team2'] < 0:
            raise serializers.ValidationError({'goals_for_team2': _('Goals cannot be negative')})
        
        if 'goals_against_team2' in attrs and attrs['goals_against_team2'] < 0:
            raise serializers.ValidationError({'goals_against_team2': _('Goals cannot be negative')})
        
        return attrs
    
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
            
            # Set verification status to pending_verification when completed
            instance.verification_status = 'pending_verification'
            instance.save()
        
        return instance


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Verification Example',
            value={
                'verified': True,
                'verification_status': 'verified',
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
    verification_status = serializers.ChoiceField(
        choices=Score.VERIFICATION_STATUS_CHOICES,
        required=False
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    
    def validate(self, attrs):
        # Only allow verification if the score is in completed status
        score = self.instance
        if score.status != 'completed':
            raise serializers.ValidationError({
                'verified': _('Cannot verify a score that is not in completed status')
            })
        
        # Verify that the verification status is valid
        if 'verification_status' in attrs and attrs['verified']:
            if attrs['verification_status'] not in ['verified', 'pending_verification']:
                raise serializers.ValidationError({
                    'verification_status': _('Invalid verification status for a verified score')
                })
        
        if 'verification_status' in attrs and not attrs['verified']:
            if attrs['verification_status'] not in ['unverified', 'disputed']:
                raise serializers.ValidationError({
                    'verification_status': _('Invalid verification status for an unverified score')
                })
        
        return attrs
    
    def update(self, instance, validated_data):
        if validated_data.get('verified'):
            instance.verified_by = self.context['request'].user
            instance.verified_at = timezone.now()
            
            # Set verification status if provided, otherwise default to 'verified'
            if 'verification_status' in validated_data:
                instance.verification_status = validated_data['verification_status']
            else:
                instance.verification_status = 'verified'
            
            if 'notes' in validated_data and validated_data['notes']:
                instance.notes = instance.notes + '\nVerification: ' + validated_data['notes']
        else:
            instance.verified_by = None
            instance.verified_at = None
            
            # Set verification status if provided, otherwise default to 'unverified'
            if 'verification_status' in validated_data:
                instance.verification_status = validated_data['verification_status']
            else:
                instance.verification_status = 'unverified'
            
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
                'assisted_by': '3fa85f64-5717-4562-b3fc-2c963f66afb3',
                'assisted_by_name': 'David Smith',
                'points': 1,
                'event_type': 'goal',
                'time_occurred': '00:15:30',
                'minute': 15,
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
    assisted_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ScoreDetail
        fields = [
            'id', 'score', 'team', 'team_name', 'player', 'player_name',
            'assisted_by', 'assisted_by_name', 'points', 'event_type',
            'time_occurred', 'minute', 'period', 'description', 'video_url'
        ]
        read_only_fields = ['id']
    
    def get_player_name(self, obj):
        if obj.player:
            return f"{obj.player.first_name} {obj.player.last_name}"
        return None
    
    def get_assisted_by_name(self, obj):
        if obj.assisted_by:
            return f"{obj.assisted_by.first_name} {obj.assisted_by.last_name}"
        return None


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Score Detail Create Example',
            value={
                'team': '3fa85f64-5717-4562-b3fc-2c963f66afa8',
                'player': '3fa85f64-5717-4562-b3fc-2c963f66afb2',
                'assisted_by': '3fa85f64-5717-4562-b3fc-2c963f66afb3',
                'points': 1,
                'event_type': 'goal',
                'time_occurred': '00:15:30',
                'minute': 15,
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
            'score', 'team', 'player', 'assisted_by', 'points', 'event_type',
            'time_occurred', 'minute', 'period', 'description', 'video_url'
        ]
    
    def validate(self, attrs):
        # Ensure score is provided when not in nested URL context
        if 'score' not in attrs and 'score' not in self.context:
            raise serializers.ValidationError({'score': _('The score field is required.')})
        
        # Ensure minute is valid if provided
        if 'minute' in attrs and attrs['minute'] is not None:
            if attrs['minute'] < 0:
                raise serializers.ValidationError({'minute': _('Minute cannot be negative')})
        
        # Ensure points are positive
        if 'points' in attrs and attrs['points'] <= 0:
            raise serializers.ValidationError({'points': _('Points must be positive')})
        
        # Get the score either from attrs or context
        score = attrs.get('score') or self.context.get('score')
        
        # Ensure team is part of the game
        team = attrs.get('team')
        if score and team:
            # Get teams from game_teams relations
            game_teams = score.game.game_teams.all()
            team_ids = [gt.team.id for gt in game_teams]
            
            if team.id not in team_ids:
                raise serializers.ValidationError(
                    {'team': _('This team is not participating in the game.')}
                )
        
        # Ensure player belongs to the selected team
        player = attrs.get('player')
        team = attrs.get('team')
        if team and player and player.team.id != team.id:
            raise serializers.ValidationError(
                {'player': _('This player does not belong to the selected team.')}
            )
        
        # Ensure assisted_by player belongs to the same team if provided
        assisted_by = attrs.get('assisted_by')
        if team and assisted_by and assisted_by.team.id != team.id:
            raise serializers.ValidationError(
                {'assisted_by': _('The assisting player must belong to the same team.')}
            )
        
        return attrs
    
    def create(self, validated_data):
        # If score is not in validated_data but in context, add it
        if 'score' not in validated_data and 'score' in self.context:
            validated_data['score'] = self.context['score']
            
        # Set created_by from context
        if 'request' in self.context:
            validated_data['created_by'] = self.context['request'].user
            
        return super().create(validated_data)


class ScoreCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a score record.
    It requires the game_id and status to create a new score.
    """
    class Meta:
        model = Score
        fields = ['game', 'status', 'scorekeeper']
    
    def validate_game(self, value):
        # Ensure that the game exists and is in a valid state
        if value is None:
            raise serializers.ValidationError(_("Game must be provided."))
        
        # Check if score already exists for this game
        if Score.objects.filter(game=value).exists():
            raise serializers.ValidationError(_("A score record already exists for this game."))
        
        # Check if game has teams assigned
        if not hasattr(value, 'game_teams') or value.game_teams.count() < 2:
            raise serializers.ValidationError(_("Game must have at least two teams assigned."))
        
        return value
    
    def validate_status(self, value):
        # Ensure the status is valid for a new score
        if value not in ['pending', 'in_progress']:
            raise serializers.ValidationError(
                _("New scores can only be created with 'pending' or 'in_progress' status.")
            )
        return value
    
    def validate_scorekeeper(self, value):
        # Ensure the scorekeeper has the correct role
        if value and value.role != 'scorekeeper':
            raise serializers.ValidationError(_("The assigned user must have the scorekeeper role."))
        return value
    
    def create(self, validated_data):
        # Create the score record
        score = Score.objects.create(**validated_data)
        
        # Initialize score as 0-0
        score.final_score_team1 = 0
        score.final_score_team2 = 0
        score.save()
   
        return score

class TeamScoreboardSerializer(serializers.Serializer):
    team = serializers.CharField()
    wins = serializers.IntegerField()
    losses = serializers.IntegerField()
    total_points = serializers.IntegerField()
    goals_for = serializers.IntegerField()
    goals_against = serializers.IntegerField()
    goal_difference = serializers.IntegerField()
    games_played = serializers.IntegerField()
    win_percentage = serializers.FloatField()
    points_per_game = serializers.FloatField()
    goals_per_game = serializers.FloatField()
    goals_against_per_game = serializers.FloatField()
    clean_sheets = serializers.IntegerField()
    yellow_cards = serializers.IntegerField()
    red_cards = serializers.IntegerField()
    fouls_committed = serializers.IntegerField()
    fouls_suffered = serializers.IntegerField()
    corners = serializers.IntegerField()
    shots = serializers.IntegerField()
    shots_on_target = serializers.IntegerField()
    