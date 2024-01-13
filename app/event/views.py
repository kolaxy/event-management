from django.shortcuts import render
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Organization, Event
from .serializers import OrganizationSerializer, EventSerializer

class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

class CustomEventPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'

class EventListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [OrderingFilter, SearchFilter]
    ordering_fields = ['date']
    search_fields = ['title']
    pagination_class = CustomEventPagination