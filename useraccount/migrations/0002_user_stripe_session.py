# Generated by Django 4.2 on 2023-05-01 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='stripe_session',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
