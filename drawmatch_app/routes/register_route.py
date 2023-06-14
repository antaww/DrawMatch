import json

from django.http import HttpRequest, HttpResponse

from drawmatch_app.models import Users


def main(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse('Only POST requests are supported', status=400)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    password = body['password']
    if not username or not password:
        return HttpResponse('Username and password must be provided', status=400)
    if Users.objects.filter(name=username).exists():
        return HttpResponse('User already exists', status=400)
    Users.objects.create(
        name=username,
        password=password
    )
    return HttpResponse('User created successfully', status=200)
