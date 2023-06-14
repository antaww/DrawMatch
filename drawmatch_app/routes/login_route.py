import json
import uuid

from django.http import HttpRequest, HttpResponse

from drawmatch_app.models import Users, Sessions


def main(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse('Only POST requests are supported', status=400)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    username = body['username']
    password = body['password']
    if not username or not password:
        return HttpResponse('Username and password must be provided', status=400)
    if not Users.objects.filter(name=username).exists():
        return HttpResponse('User does not exist', status=400)
    user = Users.objects.get(name=username)
    if user.password != password:
        return HttpResponse('Incorrect password', status=400)
    try:
        session_id = uuid.uuid4()
        Sessions.objects.create(
            user=user,
            id=session_id
        )
        response = HttpResponse('Successfully logged in', status=200)
        response.set_cookie(key='session_id', value=session_id)
        return response
    except Exception as e:
        print(e)
        return HttpResponse('Error while logging in', status=500)
