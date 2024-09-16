from django.shortcuts import render, redirect
from .forms import EventForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Event
from django.db.models import Q



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
