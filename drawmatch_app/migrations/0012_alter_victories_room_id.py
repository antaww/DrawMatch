# Generated by Django 4.2.1 on 2023-06-18 21:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('drawmatch_app', '0011_victories_room_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='victories',
            name='room_id',
            field=models.ForeignKey(default='default', on_delete=django.db.models.deletion.CASCADE, related_name='room_id', to='drawmatch_app.activerooms'),
        ),
    ]
