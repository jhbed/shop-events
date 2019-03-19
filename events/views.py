import os
from .forms import CommentForm, ImageForm
from django.utils import timezone
from django.contrib import messages
from django_proj.common.util.geo import get_distance
from django_proj.common.util.subdomain_utils import subdomain_from_request
import googlemaps
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from .models import Event, Announcement, EventAnnouncement, Comment, EventImage
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

class GetSubDomain(View):
    '''this view is just meant to test subdomain functionality'''

    def get(self, request, *args, **kwargs):
        return HttpResponse(subdomain_from_request(request))
        #return HttpResponse('hi')


class PostImage(View):

    def post(self, request, *args, **kwargs):
        form = ImageForm(request.POST or None, request.FILES or None)

        if request.user.is_authenticated:
            if not form.is_valid():
                return HttpResponse('invalid image...')
            else:
                event_pk = form.cleaned_data['event']
                img = form.cleaned_data['image']
                event = Event.objects.get(pk=event_pk)
                event_image = EventImage(image=img, event=event, posted_by=request.user)
                event_image.save()
                return redirect('event-detail', event_pk)

        else:
            if not form.is_valid():
                return HttpResponse('invalid image...')
            else:
                event_pk = form.cleaned_data['event']
                messages.error(request, 'Must be logged in to post a picture')
                return redirect('event-detail', event_pk)
        



class PostComment(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('This page is not available.')

    def post(self, request, *args, **kwargs):

        form = CommentForm(request.POST)

        if request.user.is_authenticated:
            if not form.is_valid():
                return HttpResponse('invalid comment...')
            else:
                comment = form.cleaned_data['comment']
                event_pk = form.cleaned_data['event']
                event = Event.objects.get(pk=event_pk)
                user = request.user 
                comment_obj = Comment(text=comment, event=event, user=user)
                comment_obj.save()
                return redirect('event-detail', event_pk)
        else:
            if not form.is_valid():
                return HttpResponse('invalid comment...')
            else:
                event_pk = form.cleaned_data['event']
                messages.error(request, 'Must be logged in to comment')
                return redirect('event-detail', event_pk)




            

class CompareLatLon(View):

    def get(self, request, *args, **kwargs):
        return HttpResponse('only accessible from post')

    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:
            MAX_DIST_FROM_EVENT = 2 #expressed in km
            event = Event.objects.get(pk=request.POST['event_pk'])
            lat = float(request.POST['latitude'])
            lon = float(request.POST['longitude'])
            c1 = (float(event.latitude), float(event.longitude))
            c2 = (lat, lon)
            dist = get_distance(c1, c2)
            if dist < 2:
                event.checked_in.add(request.user)
                s = 'Successfully checked you in'
                #messages.success(request, s)
                return HttpResponse(s)
            else:
                e = 'You must be within 1 mile from the event to check in!'
                #messages.error(request, e)
                return HttpResponse(e)
        else:
            e = 'You must be logged in to check in to the event.'
            #messages.error(request, e)
            return HttpResponse(e)

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

        #today = timezone.now().date()
        #event_is_today = today == event.event_date
        #event_is_passed = today > event.event_date
        data = {
            'event' : event.pk
        }
        form = CommentForm(initial=data)
        image_form = ImageForm(initial=data)
        if event.image.name != 'default_event_img.jpg':
            images = [event.image] + [img.image for img in event.event_images.all()]
        else: 
            images = [img.image for img in event.event_images.all()]
        context = {
            'object' : event,
            'attendees_count' : event.attendees.count(),
            'check_in_count' : event.checked_in.count(),
            'width_ratio' : width_ratio,
            'gmaps_key' : os.environ.get('GMAPS_API_KEY'),
            'location' : location,
            'event_day' : event.event_date.day,
            'event_month' : event.event_date.month,
            'event_year' : event.event_date.year,
            'form' : form,
            'images' : images,
            'image_form' : image_form
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
        gmaps = googlemaps.Client(key=os.environ.get('GMAPS_GEO_API_KEY'))
        geocode_result = gmaps.geocode(form.instance.location)
        data = geocode_result[0]
        form.instance.formatted_address = data['formatted_address']
        form.instance.latitude = data['geometry']['location']['lat']
        form.instance.longitude = data['geometry']['location']['lng']
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







def test(request):
    return render(request, 'events/about.html')