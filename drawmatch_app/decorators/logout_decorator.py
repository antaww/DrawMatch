from django.http import HttpResponseRedirect

from drawmatch_app.models import Sessions


def custom_logout_required(function):
    def wrap(request, *args, **kwargs):
        session_id = request.COOKIES.get('session_id')
        if session_id and Sessions.objects.filter(id=session_id).exists():
            return HttpResponseRedirect("/")
        return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
