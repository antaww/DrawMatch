# Generated by Django 4.2.1 on 2023-06-18 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('drawmatch_app', '0009_alter_victories_room_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='victories',
            name='room_id',
        ),
    ]