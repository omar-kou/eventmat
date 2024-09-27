from django.urls import path
from django.contrib import admin
from django.urls import path
from events import views 
from events.views import EventListView, EventCreateView, EventUpdateView, EventDeleteView, custom_login, signup, home
from django.contrib.auth.views import LogoutView
from django.urls import path
from events.views import CustomEventListView
urlpatterns = [
    path('', home, name='home'),
    path('login/', custom_login, name='login'),
    path('signup/', signup, name='signup'),
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/new/', EventCreateView.as_view(), name='event_create'),
    path('events/<int:pk>/edit/', EventUpdateView.as_view(), name='event_update'),
    path('events/<int:pk>/delete/', EventDeleteView.as_view(), name='event_delete'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),  # Ajoutez cette ligne pour l'admin
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'), 
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),  # Détails de l'événement
     path('custom-events/', CustomEventListView.as_view(), name='custom_event_list'),  # Nouvelle URL pour la liste personnalisée
    path('events/<int:event_id>/', views.event_detail, name='event_detail'),
    path('events/register/<int:event_id>/', views.event_register, name='event_register'),  # URL pour l'inscription à un événement
    path('events/<int:event_id>/register/', views.register_for_event, name='register_for_event'),  # Inscription à un événement
]
