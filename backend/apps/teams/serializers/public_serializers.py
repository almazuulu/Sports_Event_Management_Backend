from rest_framework import serializers
from teams.models import Team


class PublicTeamSerializer(serializers.ModelSerializer):
    """
    Serializer for limited team information to be shown publicly.
    """
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    captain_name = serializers.SerializerMethodField()
    active_player_count = serializers.IntegerField(source='players.filter(is_active=True).count', read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'logo', 'manager_name', 'captain_name', 'active_player_count']
    
    def get_captain_name(self, obj):
        if obj.team_captain:
            return obj.team_captain.get_full_name()
        return None
