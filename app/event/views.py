import datetime
import os
from django.shortcuts import render
from django.utils import timezone
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from event.tasks import create_event_with_delay
from .models import Organization, Event
from .serializers import OrganizationSerializer, OrganizationCreateSerializer, EventSerializer, EventCreateSerializer

CELERY_WAIT_TIME = os.getenv('CELERY_WAIT_TIME')

class OrganizationCreateView(generics.CreateAPIView):
    queryset = Organization.objects.all()
    serializer_class = OrganizationCreateSerializer

    def perform_create(self, serializer):
        serializer.save(founder=self.request.user)

    permission_classes = [IsAuthenticated]

class OrganizationDetailView(generics.RetrieveAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Organization.objects.all()

    def get_object(self):
        organization_id = self.kwargs.get('pk')
        event = Organization.objects.get(id=organization_id)
        return event
    
    def put(self, request, *args, **kwargs):
        organization = self.get_object()
        organization.members.add(self.request.user)
        organization.save()
        serializer = self.get_serializer(organization)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
class OrganizationListView(generics.ListAPIView):
    queryset = Event.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]

class EventCreateView(generics.CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]
    
    def create(self, request, *args, **kwargs):
        event_data = self.request.data
        required_fields = ("description", "date", "title", "organization", "image")
        
        if all(field in event_data for field in required_fields):
            organization_id = event_data.get("organization")
            
            try:
                organization = Organization.objects.get(id=organization_id, founder=self.request.user)
            except Organization.DoesNotExist:
                return Response({"message": "Invalid organization or you are not founder."}, status=status.HTTP_400_BAD_REQUEST)

            data_for_celery_task = {
                "description": event_data.get("description"),
                "date": event_data.get("date"),
                "title": event_data.get("title"),
            }
            
            data_for_celery_task["organizations"] = [organization.id]
            create_event_with_delay.apply_async((data_for_celery_task,), countdown=int(CELERY_WAIT_TIME))

            response_msg = f'Event was accepted. Wait for {str(CELERY_WAIT_TIME)} seconds.'
            return Response({'message': response_msg}, status=status.HTTP_202_ACCEPTED)
        else:
            return Response({"message": "organization, description, date, title fields needed"}, status=status.HTTP_400_BAD_REQUEST)

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
    

class EventDetailView(generics.RetrieveAPIView):
    serializer_class = EventCreateSerializer
    permission_classes = [IsAuthenticated]
    queryset = Event.objects.all()

    def get_object(self):
        event_id = self.kwargs.get('pk')
        event = Event.objects.get(id=event_id)
        return event