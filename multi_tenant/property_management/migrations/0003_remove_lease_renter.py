# Generated by Django 5.1.1 on 2024-11-10 10:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('property_management', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lease',
            name='renter',
        ),
    ]
