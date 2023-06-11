from django.http import HttpResponse

from drawmatch_app.models import ActiveRooms


def generate_room_code():
    import random
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def main(request):
    room_code = generate_room_code()
    while ActiveRooms.objects.filter(pk=room_code).exists():
        room_code = generate_room_code()
    try:
        ActiveRooms.objects.create(
            id=room_code,
            id_user_left=None,
            id_user_right=None
        )
        return HttpResponse(room_code, status=200)
    except Exception as e:
        print(e)
        return HttpResponse('Error while creating room', status=500)
