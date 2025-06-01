from django.shortcuts import redirect
from django.contrib.auth import logout

from django.contrib import messages
from .models import Teacher




def teacher_login(url):
    def decorator(fun):
        def wrap(request,*args,**kwargs):
            user = request.user
            if user.is_authenticated:
                if Teacher.objects.filter(user=user).exists():
                    return fun(request,*args,**kwargs)
                else:
                    logout(request)
                    messages.error(request,'FORBIDDEN TO ENTER HERE')
                    return redirect(url)
            else:
                return redirect(url)
        return wrap
    return decorator