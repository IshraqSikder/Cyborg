from rest_framework import serializers
from .models import Library
from user.models import Profile
from user.serializers import ProfileSerializer
from games.serializers import GameSerializer

class LibrarySerializer(serializers.ModelSerializer):
    # account = serializers.StringRelatedField(many=False)
    # game = serializers.StringRelatedField(many=False)
    # account = ProfileSerializer(many=False, read_only=True)
    # game = GameSerializer(many=False, read_only=True)
    accountName = serializers.SerializerMethodField()
    gameDetails = serializers.SerializerMethodField()
    class Meta:
        model = Library
        fields = '__all__'
        
    def get_accountName(self, obj):
        account = obj.account
        if account and hasattr(account, 'userName'):
            return account.userName.username
        return None

    def get_gameDetails(self, obj):
        game = obj.game
        if game:
            return {
                'title': game.title,
                'genre': game.genre,
                'image': self.context['request'].build_absolute_uri(game.image.url) if game.image else None
            }
        return None