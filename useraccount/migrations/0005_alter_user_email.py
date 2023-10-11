# Generated by Django 4.2.1 on 2023-10-11 01:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('useraccount', '0004_user_stripe_customer_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address'),
        ),
    ]