from django.shortcuts import render
from rest_framework import viewsets, filters, pagination
from .models import Stream
from .serializers import StreamSerializer
from django_filters.rest_framework import DjangoFilterBackend
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
        
class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title']
    filterset_fields = ['streamer', 'game']
    pagination_class = CustomPagination
    
@api_view(['GET'])
def game_list(request):
    games = Stream.objects.values('game__id', 'game__title').distinct()
    return Response(games)

@api_view(['GET'])
def streamer_list(request):
    streamers = Stream.objects.values('streamer__id', 'streamer__userName__username').distinct()
    return Response(streamers)