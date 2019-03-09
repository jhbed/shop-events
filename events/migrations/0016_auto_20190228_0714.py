# Generated by Django 2.1.7 on 2019-02-28 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0015_auto_20190228_0700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='address',
        ),
        migrations.AddField(
            model_name='event',
            name='formatted_address',
            field=models.CharField(default='1600 Amphitheatre Parkway, Mountain View, CA 94043, USA', max_length=500),
        ),
        migrations.AddField(
            model_name='event',
            name='latitude',
            field=models.FloatField(default=47.6205),
        ),
        migrations.AddField(
            model_name='event',
            name='longitude',
            field=models.FloatField(default=122.3493),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]