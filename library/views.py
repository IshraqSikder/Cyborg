from django.shortcuts import render
from rest_framework import viewsets, filters, status
from .models import Library
from .serializers import LibrarySerializer
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse

# Create your views here.
# class SearchByAccountAndGame(filters.BaseFilterBackend):
#     def filter_queryset(self, request, queryset, view):
#         # account = request.query_params.get("account")
#         # if account:
#         #     return query_set.filter(account = account)
#         # return query_set
#         account_id = request.query_params.get('account')
#         game_id = request.query_params.get('game')
#         if account_id:
#             queryset = queryset.filter(account__id=account_id)
#         if game_id:
#             queryset = queryset.filter(game__id=game_id)
#         return queryset
    
class LibraryViewSet(viewsets.ModelViewSet):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['account', 'game']
    # permission_classes = [IsAuthenticated]

    # def get_queryset(self):
    #     return Library.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError as err:
            if 'UNIQUE constraint failed' in str(err):
                raise ValidationError({'detail': 'This game is already added to the library for this account.'})
            else:
                raise err
    
    def remove_from_library(request):
        library_id = request.GET.get('library_id')
        if library_id:
            library_item = get_object_or_404(Library, id=library_id)
            library_item.delete()
            return JsonResponse({'status': 'success', 'message': 'Game removed successfully'})
        return JsonResponse({'status': 'error', 'message': 'Invalid library ID'})