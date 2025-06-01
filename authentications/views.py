from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login
from django.views.decorators.cache import never_cache
from django.contrib import messages
from .decorator import teacher_login
from django.http import JsonResponse
from .models import Marks,Student
import json
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.utils import timezone

def login_view(request):
    if request.method == "POST":
        user_name = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=user_name, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")  
        else:
            messages.error(request, "Invalid username or password")
            return redirect(login_view)


        
    return render(request=request,template_name="login/login.html")

@never_cache
@teacher_login(url="/login") 
def home_view(request):
    
    return render(request=request,template_name="home/home.html")

def return_data_student(request):

    marks = Marks.objects.all().values("id","student__name","subject","marks_obtained",)
    
    return JsonResponse({"data":json.dumps(list(marks))})

@csrf_exempt
def update_student(request):
    
    data = json.loads(request.body)
    if Marks.objects.filter(subject=data.get("subject"),student__name=data.get("name")).exclude(id=data.get("id")).exists():
        return JsonResponse({"status":"user with same subject exist"})
    try:
        mark_obj = Marks.objects.get(id=data.get("id"))
    except Marks.DoesNotExist:
        return JsonResponse({"status":"data not found"})
    except Exception:
        return JsonResponse({"status":"Un found error"})
    with transaction.atomic():
        mark_obj.mark = data.get("mark")
        mark_obj.subject = data.get("subject")
        mark_obj.student.name = data.get("name")
        mark_obj.marks_obtained = data.get("mark")
        mark_obj.student.save()
        mark_obj.save()
    return JsonResponse({"status":"success"})

@csrf_exempt
def add_student_mark(request):
    data = json.loads(request.body)
    student_q = Marks.objects.filter(subject=data.get("subject"),student__name=data.get("name"))
    if student_q.exists():
        student = student_q.first()
        student.marks_obtained = data.get("mark")
        student.save()
        return JsonResponse({"status":"success"})
    try:
        stuendt_objec = Student.objects.get(name=data.get("name"))
    except Exception:
        return JsonResponse({"status":"failed"})
    Marks.objects.create(subject=data.get("subject"),marks_obtained=data.get("mark"),student=stuendt_objec,classroom=stuendt_objec.current_classroom,date=timezone.now())
    
    return JsonResponse({"status":"success"})
