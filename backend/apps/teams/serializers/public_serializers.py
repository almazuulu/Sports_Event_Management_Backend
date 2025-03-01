# serializers.py (Teams app)
from rest_framework import serializers
from teams.models import Team

class PublicTeamSerializer(serializers.ModelSerializer):
    """
    Serializer for limited team information to be shown publicly.
    """
    captain_name = serializers.CharField(source='captain.get_full_name', read_only=True)
    active_player_count = serializers.IntegerField(source='players.filter(is_active=True).count', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'captain_name', 'active_player_count']
