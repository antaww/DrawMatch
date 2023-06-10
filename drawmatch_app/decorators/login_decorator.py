from django.shortcuts import redirect

from drawmatch_app.models import Sessions


def custom_login_required(function):
    def wrap(request, *args, **kwargs):
        session_id = request.COOKIES.get('session_id')
        if session_id:
            try:
                session = Sessions.objects.get(id=session_id)
                request.user = session.user
                return function(request, *args, **kwargs)
            except Sessions.DoesNotExist:
                pass
        return redirect('/login/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
