from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='events')
    rsvp_goal = models.IntegerField(verbose_name="Attendees Goal")
    image = models.ImageField(default='default_event_img.jpg', upload_to='event_pics', verbose_name='Event Image')
    event_date = models.DateField()

    def __str__(self):
        return self.title

    #this is the method we need to define to get the absolute url of this object
    #this structure below takes us to event-detail url pattern, plugging in pk where pk 
    #falls in the pattern. In this case event/pk
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk' : self.pk})


class Announcement(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class EventAnnouncement(models.Model):
    text = models.TextField()
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.text



