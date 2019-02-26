from django.urls import path
from . import views
from .views import (EventListView, 
                    EventDetailView, 
                    EventCreateView, 
                    EventUpdateView, 
                    EventDeleteView,
                    UserEventListView,
                    EventAnnouncementUpdateView,
                    EventAnnouncementCreateView)

urlpatterns = [
    path('', view=EventListView.as_view(), name='events-home'),
    path('user/<str:username>/', view=UserEventListView.as_view(), name='user-events'),
    path('event/<int:pk>/', view=EventDetailView.as_view(), name='event-detail'),
    path('event/<int:pk>/update', view=EventUpdateView.as_view(), name='event-update'),
    path('event/announcement/<int:pk>/update', view=EventAnnouncementUpdateView.as_view(), name='update-event-announcement'),
    path('event/announcement/new/', view=EventAnnouncementCreateView.as_view(), name='create-event-announcement'),
    path('event/<int:pk>/delete', view=EventDeleteView.as_view(), name='event-delete'),
    path('event/new/', view=EventCreateView.as_view(), name='event-create'),
    path('about/', views.about, name='about')
]
