from django.urls import path
from django.contrib import admin
from django.urls import path
from events import views 
from events.views import EventListView, EventCreateView, EventUpdateView, EventDeleteView, custom_login, signup, home
from django.contrib.auth.views import LogoutView
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
     
]
