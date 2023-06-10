from django.http import HttpRequest, HttpResponse, HttpResponseRedirect

from drawmatch_app.models import Sessions


def main(request: HttpRequest) -> HttpResponse:
    session_id = request.COOKIES.get('session_id')
    if session_id:
        try:
            session = Sessions.objects.get(id=session_id)
            session.delete()
        except Sessions.DoesNotExist:
            pass
        response = HttpResponseRedirect('/')
        response.delete_cookie('session_id')
        return response
