from django.shortcuts import render
from rest_framework import viewsets, filters, pagination
from .models import Game
from .serializers import GameSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
class CustomPagination(pagination.PageNumberPagination):
    page_size = 8
    page_size_query_param = 'page_size'
    max_page_size = 100
    
    # It is used to add page_size to the response
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
            'page_size': self.page_size
        })
       
class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'owner', 'genre']
    ordering_fields = ['rating', 'download_count', 'size', 'release_date']
    # ordering = ['rating']
    pagination_class = CustomPagination
    
@api_view(['GET'])
def genre_list(request):
    genres = Game.objects.values_list('genre', flat=True).distinct()
    return Response(genres)
    