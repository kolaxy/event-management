import datetime
from django.shortcuts import render
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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

    def get_queryset(self):
        queryset = super().get_queryset()

        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            try:
                start_date = timezone.make_aware(timezone.datetime.strptime(start_date, '%Y-%m-%d'))
                end_date = timezone.make_aware(timezone.datetime.strptime(end_date, '%Y-%m-%d'))
                queryset = queryset.filter(date__range=(start_date, end_date))
            except ValueError:
                return Response({'error': 'Invalid date format'}, status=400)

        return queryset