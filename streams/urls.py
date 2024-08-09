from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StreamViewSet, game_list, streamer_list

router = DefaultRouter()
router.register('list', StreamViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('games/', game_list, name='game-list'),
    path('streamers/', streamer_list, name='streamer-list'),
]