import json

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse


def get_room_code(request) -> str:
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    room_code = body['room_code']
    return room_code


def store_drawing(request):
    room_code = get_room_code(request)
    if request.method != 'POST':
        return HttpResponse('Only POST requests are supported', status=400)
    body_unicode = request.body.decode('utf-8')
    loaded_json = json.loads(body_unicode)
    data = loaded_json['array']
    cache_key = f'drawing-{room_code}'

    if cache.has_key(cache_key):
        old_data = cache.get(cache_key)
        data = old_data + data

    cache.set(cache_key, data, 600)  # 10 minutes cache (to avoid memory leak)
    return JsonResponse({'status': 'ok'})


def get_drawing(request):
    room_code = get_room_code(request)
    cache_key = f'drawing-{room_code}'
    data = cache.get(cache_key)
    if data is None:
        return JsonResponse({'status': 'not found'})
    return JsonResponse({'status': 'ok', 'map': data})

# todo: clear draw
