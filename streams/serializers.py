from rest_framework import serializers
from .models import Stream
from games.serializers import GameSerializer

class StreamSerializer(serializers.ModelSerializer):
    # game = serializers.StringRelatedField(many=False)
    # game = GameSerializer(many=False, read_only=True)
    # streamer = serializers.StringRelatedField(many=False)
    streamerDetails = serializers.SerializerMethodField()
    gameDetails = serializers.SerializerMethodField()
    class Meta:
        model = Stream
        fields = '__all__'
        
    def get_streamerDetails(self, obj):
        streamer = obj.streamer
        if streamer and hasattr(streamer, 'userName'):
            # return streamer.userName.username
            return {
                'streamer': streamer.userName.username,
                'avatar': streamer.avatar.url
            }
        return None
        
    def get_gameDetails(self, obj):
        game = obj.game
        if game:
            return {
                'title': game.title,
                'genre': game.genre
            }
        return None