from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import GameViewSet, genre_list

router = DefaultRouter()
router.register('list', GameViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('genres/', genre_list, name='genre-list'),
]