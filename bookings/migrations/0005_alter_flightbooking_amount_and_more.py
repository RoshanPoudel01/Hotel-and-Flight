# Generated by Django 4.2.1 on 2023-07-15 12:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_flightbooking'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flightbooking',
            name='amount',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='flightbooking',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
