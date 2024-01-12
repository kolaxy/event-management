# myapp/urls.py

from django.urls import path
from .views import OrganizationCreateView, EventCreateView, EventListView

urlpatterns = [
    path('create-organization/', OrganizationCreateView.as_view(), name='create-organization'),
    path('create-event/', EventCreateView.as_view(), name='create-event'),
    path('event-list/', EventListView.as_view(), name='event-list'),
]
