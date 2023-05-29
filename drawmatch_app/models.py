from django.db import models
from django.contrib.auth.models import User


class Room(models.Model):
    code = models.CharField(max_length=10, unique=True)
    room_owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='salons_crees')

    def __str__(self):
        return self.code


class Draw(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='dessins')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='draws/')
    correspondence = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Dessin du salon {self.room.code} par {self.user.username}"
