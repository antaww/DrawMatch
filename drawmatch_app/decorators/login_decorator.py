from django.shortcuts import redirect


def custom_login_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return function(request, *args, **kwargs)
        else:
            return redirect('/login/')

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
