from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.
# class Address(models.Model):
#     street_number = models.CharField(max_length=100)
#     street = models.CharField(max_length=300)
#     city = models.CharField(max_length=200)
#     county = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     country = models.CharField(max_length=100)
#     zip_code = models.CharField(max_length=100)
#     formatted_address = models.CharField(max_length=400)
#     latitude = models.FloatField(default=47.6205)
#     longitude = models.FloatField(default=122.3493)

    # def __str__(self):
    #     return self.formatted_address



class Event(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    attendees = models.ManyToManyField(User, related_name='events')
    checked_in = models.ManyToManyField(User, related_name='events_attended')
    rsvp_goal = models.IntegerField(verbose_name="Attendees Goal")
    image = models.ImageField(default='default_event_img.jpg', upload_to='event_pics', verbose_name='Event Image')
    event_date = models.DateField()
    location = models.CharField(max_length=500)
    #address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    formatted_address = models.CharField(max_length=500, default="1600 Amphitheatre Parkway, Mountain View, CA 94043, USA")
    latitude = models.FloatField(default=47.6205)
    longitude = models.FloatField(default=122.3493)
    #how much battery (in miles) a persons electric scateboard needs to be able to go
    continuous_charge_miles_needed = models.FloatField(default=0.0)
    #beginner, intermediate, advanced, etc
    skill_level = models.CharField(max_length=200, default='Beginner')


    def __str__(self):
        return self.title

    #this is the method we need to define to get the absolute url of this object
    #this structure below takes us to event-detail url pattern, plugging in pk where pk 
    #falls in the pattern. In this case event/pk
    def get_absolute_url(self):
        return reverse('event-detail', kwargs={'pk' : self.pk})

    def get_fb_url(self):
        string = reverse('event-detail', kwargs={'pk' : self.pk})
        string.replace('/', '%2F')



class Announcement(models.Model):
    text = models.TextField()

    def __str__(self):
        return self.text

class EventAnnouncement(models.Model):
    text = models.TextField()
    event = models.OneToOneField(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

class Comment(models.Model):
    text = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')

class EventImage(models.Model):
    image = models.ImageField(default='default_event_img.jpg', upload_to='event_pics', verbose_name='Event Image')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_images')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='event_images_posted')

    # def save(self, *args, **kwargs):
    #     import os
    #     from PIL import Image
    #     from django.core.files.storage import default_storage as storage
    #     if not self.image:
    #         return ""
            
    #     super(EventImage, self).save(*args, **kwargs)
    #     file_path = self.image.name
    #     filename_new, filename_ext = os.path.splitext(file_path)

    #     try:
    #         # resize the original image and return url path of the thumbnail
    #         f = storage.open(file_path, 'r')
    #         image = Image.open(f)
    #         width, height = image.size

    #         if width > 300 or height > 300:
    #             output_size = (300,300)
    #             image.thumbnail(output_size)
    #             f_thumb = storage.open(filename_new, "w")
    #             image.save(f_thumb, "JPEG")
    #             f_thumb.close()
    #         return "success"
    #     except:
    #         return "error"
        





