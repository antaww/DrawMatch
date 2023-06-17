import json
import os
from random import random

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

from DrawMatch import settings

cache_duration = 600  # 10 minutes cache (to avoid memory leak)


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
    data = loaded_json['drawingsDatas']
    cache_key = f'drawing-{room_code}'

    if cache.has_key(cache_key):
        old_data = cache.get(cache_key)
        data = old_data + data

    cache.set(cache_key, data, cache_duration)
    return JsonResponse({'status': 'ok'})


def get_drawing(request):
    room_code = get_room_code(request)
    cache_key = f'drawing-{room_code}'
    data = cache.get(cache_key)
    if data is None:
        return JsonResponse({'status': 'not found'})
    return JsonResponse({'status': 'ok', 'map': data})


def generate_words(request):
    room_code = get_room_code(request)
    if cache.has_key(f'words-{room_code}'):
        return JsonResponse({'status': 'already generated'})
    labels_path = os.path.join(settings.BASE_DIR, 'drawmatch_app', 'ai_testing', 'data', 'labels.txt')
    with open(labels_path, 'r') as f:
        lines = f.readlines()
        random_lines = []
        for i in range(6):
            random_lines.append(lines[int(random() * len(lines))].strip())
    cache_key = f'words-{room_code}'
    cache.set(cache_key, random_lines, cache_duration)
    return JsonResponse({'status': 'ok'})


def get_words(request):
    room_code = get_room_code(request)
    cache_key = f'words-{room_code}'
    data = cache.get(cache_key)
    if data is None:
        return JsonResponse({'status': 'not found'})
    return JsonResponse({'status': 'ok', 'words': data})


def remove_first_word(request):
    room_code = get_room_code(request)
    cache_key = f'words-{room_code}'
    data = cache.get(cache_key)
    if data is None:
        return JsonResponse({'status': 'not found'})
    data.pop(0)
    cache.set(cache_key, data, cache_duration)
    return JsonResponse({'status': 'ok'})


def erase_drawing(request):
    room_code = get_room_code(request)
    if request.method != 'POST':
        return HttpResponse('Only POST requests are supported', status=400)
    body_unicode = request.body.decode('utf-8')
    loaded_json = json.loads(body_unicode)
    data = loaded_json['canvas']
    cache_key = f'drawing-{room_code}'
    old_data = cache.get(cache_key)
    new_data = []
    for d in old_data:
        if d['canvas'] != data:
            new_data.append(d)
    cache.set(cache_key, new_data, cache_duration)
    return JsonResponse({'status': 'ok'})
