from django import forms


class RoomForm(forms.Form):
    room_code = forms.CharField(label='Room Code', max_length=10)
