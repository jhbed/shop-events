# Generated by Django 2.1.7 on 2019-02-20 21:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_event_event_datetime'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='event_datetime',
        ),
        migrations.AddField(
            model_name='event',
            name='event_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
