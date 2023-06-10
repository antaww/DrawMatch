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
    if not Users.objects.filter(name=username).exists():
        return HttpResponse('User does not exist', status=400)
    user = Users.objects.get(name=username)
    if user.password != password:
        return HttpResponse('Incorrect password', status=400)
    return HttpResponse('User logged in successfully', status=200)
