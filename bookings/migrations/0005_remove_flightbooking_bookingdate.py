# Generated by Django 4.2.1 on 2023-07-17 03:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_flightbooking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='flightbooking',
            name='bookingdate',
        ),
    ]