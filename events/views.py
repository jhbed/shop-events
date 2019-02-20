from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Event
from django.contrib.auth.models import User
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (ListView, 
                                  DetailView, 
                                  CreateView,
                                  UpdateView,
                                  DeleteView, 
                                  View)
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
        


class EventDetailView(SingleObjectMixin, View):
    model = Event
    #template_name_suffix = '_attend_form'
    #fields = ['attendees']
    http_method_names = ['post', 'get']

    def get(self, request, *args, **kwargs):

        event = self.get_object()
        goal = event.rsvp_goal
        width_ratio = (event.attendees.count() / goal) * 100
        width_ratio = str(width_ratio) + '%'
        context = {
            'object' : event,
            'attendees_count' : event.attendees.count(),
            'width_ratio' : width_ratio
        }

        return render(request, 'events/event_detail.html', context)

    def post(self, request, *args, **kwargs):
        event = self.get_object()
        if self.request.user.is_authenticated:
            event.attendees.add(self.request.user)
            return redirect('event-detail', event.pk)
        else:
            #return the same page with modal trggered and error msg
            #below is not sufficient
            return redirect('login')
            


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
    fields = ['title', 'rsvp_goal', 'content', 'image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        #we're overriding super.form_valid(), fixing the form, then calling it, passing in the form  
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'content', 'image']

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