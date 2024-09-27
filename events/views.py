import datetime
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event
from django.db.models import Q
from .models import Event, Participant
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Event
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Event
# events/views.py
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event, Participant

@login_required
def event_register(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Vérifie si l'utilisateur est déjà inscrit
    if Participant.objects.filter(user=request.user, event=event).exists():
        # Redirige vers la page des détails de l'événement si déjà inscrit
        return redirect('event_detail', event_id=event.id)
    
    # Crée une nouvelle participation pour l'utilisateur
    Participant.objects.create(user=request.user, event=event)
    
    # Redirige vers la page des détails de l'événement après inscription
    return redirect('event_detail', event_id=event.id)


class CustomEventListView(ListView):
    model = Event
    template_name = 'custom_event_list.html'  # Nom différent pour le nouveau template
    context_object_name = 'events'  # Le nom utilisé pour accéder aux événements dans le template

    # Si vous voulez personnaliser ou filtrer la liste d'événements, vous pouvez surcharger get_queryset()
    def get_queryset(self):
        # Par exemple, vous pouvez filtrer les événements passés ou futurs
        return Event.objects.filter(date__gte=datetime.date.today())  # Affiche seulement les événements futurs


def event_detail(request, event_id):
    event = Event.objects.get(id=event_id)  # Cela pourrait causer une erreur si plusieurs événements ont le même id
    return render(request, 'event_detail.html', {'event': event})

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'



@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    # Vérifie si l'utilisateur est déjà inscrit
    if Participant.objects.filter(user=request.user, event=event).exists():
        return render(request, 'events/already_registered.html', {'event': event})
    
    # Crée l'inscription si elle n'existe pas
    Participant.objects.create(user=request.user, event=event)
    return redirect('event_detail', event_id=event.id)


class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Event.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
        return Event.objects.all()

class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_list')

    def form_valid(self, form):
        form.instance.organizer = self.request.user  # Associe l'utilisateur connecté à l'événement
        return super().form_valid(form)

def home(request):
    return render(request, 'home.html')

# Login view
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('event_list')  # Redirect to event list
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Signup view
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Event views
class EventListView(LoginRequiredMixin, ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'
    login_url = 'login'


class EventUpdateView(LoginRequiredMixin, UpdateView):
    model = Event
    form_class = EventForm
    template_name = 'event_form.html'
    success_url = reverse_lazy('event_list')
    login_url = 'login'

class EventDeleteView(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'event_confirm_delete.html'
    success_url = reverse_lazy('event_list')
    login_url = 'login'
