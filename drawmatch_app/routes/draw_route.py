import json
import os
from datetime import time
from random import random

from django.core.cache import cache
from django.http import HttpResponse, JsonResponse

from DrawMatch import settings
from drawmatch_app.models import Victories, Users, ActiveRooms

cache_duration = 1200  # 20 minutes cache (to avoid memory leak)


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
        for i in range(7):
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


def add_score(request):
    room_code = get_room_code(request)
    if request.method != 'POST':
        return HttpResponse('Only POST requests are supported', status=400)
    body_unicode = request.body.decode('utf-8')
    loaded_json = json.loads(body_unicode)
    position = loaded_json['position']
    score = loaded_json['score']
    score += 1
    cache_key = f'score-{room_code}'
    if cache.has_key(cache_key):
        old_data = cache.get(cache_key)
        old_data[position] = score
        cache.set(cache_key, old_data, cache_duration)
    else:
        cache.set(cache_key, {position: score}, cache_duration)
    return JsonResponse({'status': 'ok'})


def get_scores(request):
    room_code = get_room_code(request)
    cache_key = f'score-{room_code}'
    data = cache.get(cache_key)
    if data is None:
        return JsonResponse({'status': 'not found'})
    return JsonResponse({'status': 'ok', 'score': data})


def add_win(request):
    room_code = get_room_code(request)
    if request.method != 'POST':
        return HttpResponse('Only POST requests are supported', status=400)
    body_unicode = request.body.decode('utf-8')
    loaded_json = json.loads(body_unicode)
    winner_id = loaded_json['winner_id']
    print(winner_id)
    print(room_code)
    try:
        winner = Users.objects.get(id=winner_id)
        print(winner)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error'})

    try:
        room = ActiveRooms.objects.get(pk=room_code)
        print(room)
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error'})

    try:
        Victories.objects.create(room_id=room, user_id=winner)
        print(Victories.objects.all())
        return JsonResponse({'status': 'ok'})
    except Exception as e:
        print(e)
        return JsonResponse({'status': 'error'})
