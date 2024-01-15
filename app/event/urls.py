from django.urls import path
from .views import OrganizationCreateView, EventCreateView, EventListView, EventDetailView, OrganizationDetailView, OrganizationListView

urlpatterns = [
    path('organizations/', OrganizationListView.as_view(), name='organization-list'),
    path('organizations/create/', OrganizationCreateView.as_view(), name='create-organization'),
    path('organizations/<int:pk>', OrganizationDetailView.as_view(), name='organization-detail'),
    path('events/', EventListView.as_view(), name='event-list'),
    path('events/create/', EventCreateView.as_view(), name='create-event'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event-detail'),
]


