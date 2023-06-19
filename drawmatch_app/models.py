from django.db import models


# After creating a new model, you should first run python manage.py makemigrations to create migrations for those
# changes and then run python manage.py migrate to apply those changes to the database.


# Users table (id, name, password, created_date)
class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=50)
    created_date = models.DateTimeField(auto_now_add=True)


# ActiveRooms table (id, id_user_left, id_user_right, created_date)
class ActiveRooms(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    id_user_left = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='id_user_left', null=True)
    id_user_right = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='id_user_right', null=True)
    created_date = models.DateTimeField(auto_now_add=True)


# Points table (id, user_id, points, room_id, created_date)
class Points(models.Model):
    id = models.AutoField(primary_key=True)
    points = models.IntegerField(default=0)
    user_id = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='user_id')
    room_id = models.ForeignKey(ActiveRooms, on_delete=models.CASCADE, related_name='room_id', default='default')
    created_date = models.DateTimeField(auto_now_add=True)


# Sessions table (id, user, created_date)
class Sessions(models.Model):
    id = models.CharField(max_length=64, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sessions')
