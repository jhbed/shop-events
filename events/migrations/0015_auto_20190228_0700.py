# Generated by Django 2.1.7 on 2019-02-28 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20190228_0614'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_number', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=200)),
                ('county', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=100)),
                ('zip_code', models.CharField(max_length=100)),
                ('formatted_address', models.CharField(max_length=400)),
                ('latitude', models.FloatField(default=47.6205)),
                ('longitude', models.FloatField(default=122.3493)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='event',
            name='longitude',
        ),
        migrations.AddField(
            model_name='event',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.Address'),
        ),
    ]