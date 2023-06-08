from django.shortcuts import redirect


def custom_logout_required(function):
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return function(request, *args, **kwargs)

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap
