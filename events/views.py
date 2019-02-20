from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Event
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView)
# Create your views here.

def home(request):
    context = {
        'posts': Event.objects.all,
    }
    return render(request, 'events/home.html', context)


class EventListView(ListView):
    model = Event
    #app/model_viewtype.html
    template_name = 'events/home.html'
    context_object_name = 'events'
    ordering = ['-date_posted'] #a list of orderings (priority in front I assume). Minus sign is for descending!
    paginate_by = 8

class UserEventListView(ListView):
    model = Event
    #app/model_viewtype.html
    template_name = 'events/user_events.html'
    context_object_name = 'events'
    paginate_by = 8

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Event.objects.filter(author=user).order_by('-date_posted')
        


class EventDetailView(DetailView):
    model = Event

class EventDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Event
    success_url = '/'
    #this function is called by UserPassesTestMixin. If false, the page will lock. So if this view is called,
    #the current user must be the author
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author



class EventCreateView(LoginRequiredMixin, CreateView):
    model = Event
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        #we're overriding super.form_valid(), fixing the form, then calling it, passing in the form  
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.author = self.request.user
        #we're overriding super.form_valid(), fixing the form, then calling it, passing in the form  
        return super().form_valid(form)

    #this function is called by UserPassesTestMixin. If false, the page will lock. So if this view is called,
    #the current user must be the author
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author




def about(request):
    return render(request, 'events/about.html')