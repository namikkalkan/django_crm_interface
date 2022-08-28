from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib import messages


def unauthenticated_user(view_f):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return view_f(request, *args, **kwargs)

    return wrapper


def allowed_user(allowed_roles=[]):
    def decorator(view_f):
        def wrapper(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
                return view_f(request, *args, **kwargs)
            elif group =='employee':
                messages.warning(request, 'You are not allowed for it, please ask for admin')
                return redirect('home')
            else:
                messages.warning(request, 'You are not allowed for it, please ask for admin')
                return redirect('user_page')

        return wrapper

    return decorator


def admin_only(view_f):
    def wrapper(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('user_page')
        elif group == 'employee':
            return view_f(request, *args, **kwargs)
        elif group == 'admin':
            messages.info(request, 'Welcome on board Admin')
            return view_f(request, *args, **kwargs)

    return wrapper
