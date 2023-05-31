from django.db import models


# After creating a new model, you should first run python manage.py makemigrations to create migrations for those
# changes and then run python manage.py migrate to apply those changes to the database.


# Users table (id, name, password, victories, created_date)
class Users(models.Model):
    name = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=50)
    victories = models.IntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)


# ActiveRooms table (id, id_user_left, id_user_right, created_date)
class ActiveRooms(models.Model):
    id = models.CharField(max_length=6, primary_key=True)
    id_user_left = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='left', null=True)
    id_user_right = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='right', null=True)
    created_date = models.DateTimeField(auto_now_add=True)


# Sessions table (id, user, created_date)
class Sessions(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='sessions')
    id = models.CharField(max_length=64, primary_key=True)
    created_date = models.DateTimeField(auto_now_add=True)
