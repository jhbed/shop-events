# Generated by Django 2.1.7 on 2019-02-20 15:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_event_attendees'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='rsvp_goal',
            field=models.IntegerField(default=4),
            preserve_default=False,
        ),
    ]
