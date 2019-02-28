import os
from django_proj.common.util.geo import get_distance
import googlemaps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Event, Announcement, EventAnnouncement
from django import forms
from django.db.models import Count
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

class CompareLatLon(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('only accessible from post')

    def post(self, request, *args, **kwargs):
        
        event = Event.objects.get(pk=request.POST['event_pk'])
        lat = float(request.POST['latitude'])
        lon = float(request.POST['longitude'])
        c1 = (float(event.latitude), float(event.longitude))
        c2 = (lat, lon)
        dist = get_distance(c1, c2)
        #return HttpResponse('hello')
        return HttpResponse('distance between you and event is: ' + str(dist))
        #return redirect('login')
        #return JsonResponse({'success' : 'hi'})


class EventListView(ListView):
    model = Event
    #app/model_viewtype.html
    template_name = 'events/home.html'
    context_object_name = 'events'
    ordering = ['-date_posted'] #a list of orderings (priority in front I assume). Minus sign is for descending!
    paginate_by = 8
    extra_context = {
        #'top_event' : Event.objects.all().annotate(attendee_count=Count('attendees')).order_by('-attendee_count').first(),
        'most_active_shredder' : User.objects.all().annotate(event_count=Count('events')).order_by('-event_count').first(),
        'announcements' : Announcement.objects.all()
    }

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
        location = event.location
        location = location.replace(' ', '+')
        goal = event.rsvp_goal
        width_ratio = (event.attendees.count() / goal) * 100
        width_ratio = str(width_ratio) + '%'
        context = {
            'object' : event,
            'attendees_count' : event.attendees.count(),
            'width_ratio' : width_ratio,
            'gmaps_key' : os.environ.get('GMAPS_API_KEY'),
            'location' : location
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
    fields = ['title', 'location','rsvp_goal', 'content', 'image', 'event_date']

    def get_form(self):
        form = super().get_form()
        form.fields['rsvp_goal'].widget = forms.NumberInput(attrs={'placeholder': 5})
        form.fields['event_date'].widget = forms.TextInput(attrs={'type':'date'})
        return form

    def form_valid(self, form):
        gmaps = googlemaps.Client(key=os.environ.get('GMAPS_GEO_API_KEY'))
        geocode_result = gmaps.geocode(form.instance.location)
        data = geocode_result[0]
        form.instance.formatted_address = data['formatted_address']
        form.instance.latitude = data['geometry']['location']['lat']
        form.instance.longitude = data['geometry']['location']['lng']
        form.instance.author = self.request.user
        #we're overriding super.form_valid(), fixing the form, then calling it, passing in the form  
        return super().form_valid(form)

class EventUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Event
    fields = ['title', 'location','rsvp_goal', 'content', 'image', 'event_date']
    extra_context = {
        'update' : True
    }

    def get_form(self):
        form = super().get_form()
        form.fields['rsvp_goal'].widget = forms.NumberInput(attrs={'placeholder': 5})
        form.fields['event_date'].widget = forms.TextInput(attrs={'type':'date'})
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        #we're overriding super.form_valid(), fixing the form, then calling it, passing in the form  
        return super().form_valid(form)

    #this function is called by UserPassesTestMixin. If false, the page will lock. So if this view is called,
    #the current user must be the author
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class EventAnnouncementUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EventAnnouncement
    fields = ['text']

    def test_func(self):
        announcement = self.get_object()
        return self.request.user == announcement.event.author

    def get_success_url(self):
        announcement = self.get_object()
        return reverse_lazy('event-detail', kwargs={'pk': announcement.event.pk})

class EventAnnouncementCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EventAnnouncement
    fields = ['text']

    def test_func(self):
        event = Event.objects.get(pk=self.request.GET.get('event', ''))
        return self.request.user == event.author

    def get_success_url(self):
        event = Event.objects.get(pk=self.request.GET.get('event', ''))
        return reverse_lazy('event-detail', kwargs={'pk': event.pk})

    def form_valid(self, form):
        form.instance.event = Event.objects.get(pk=self.request.GET.get('event', ''))
        #we're overriding super.form_valid(), fixing the form, then calling it, passing in the form  
        return super().form_valid(form)







def about(request):
    return render(request, 'events/about.html')