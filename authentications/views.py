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
from django.db.models import  F
from .utils import validations
from .types import login_validator,update_mark_validator,add_student_mark_validator

def login_view(request):
    """
    Login View 
    username:str
    password:str
    response redirect-> login or home
    """
    if request.method == "POST":
        data = validations(request.POST,login_validator)
        if data.get("error_status"):
            messages.error(request=request,message=data.get("error").popitem()[1])
            return redirect(login_view)
        user = authenticate(request, username=data.get("username"), password=data.get("password"))
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
    """
    render Home protected route
    """
    return render(request=request,template_name="home/home.html")

def return_data_student(request):
    marks = Marks.objects.all().values("id","student__name","subject","marks_obtained",)   
    return JsonResponse({"data":json.dumps(list(marks))})

@csrf_exempt
def update_student(request):
    """
    update student students 
    params
    subject:str
    mark:int
    name:str


    """
    data = json.loads(request.body)

    data = validations(data=data,structer=update_mark_validator)

    if data.get("error"):
            
        return JsonResponse(
            {
            "msg":"validation erorr",
            "error":data.get("error").popitem()[1]
                              }
            )
    try:
        with transaction.atomic():
            student, created = Student.objects.get_or_create(name=data.get("name"))
    except Exception:
        JsonResponse(
            {
                "msg":"student with name already exist"

            },
            status=400
        )
            

    if Marks.objects.filter(subject=data.get("subject"),student=student).exclude(id=data.get("id")).exists():
        return JsonResponse({"status":"user with same subject exist"},status=400)
    try:
        mark_obj = Marks.objects.get(id=data.get("id"))
    except Marks.DoesNotExist:
        return JsonResponse({"status":"data not found"},status=400)
    except Exception:
        return JsonResponse({"status":"Unfound error"},status=400)
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
    data = validations(data=data,structer=add_student_mark_validator)
    if data.get("error"):
            
        return JsonResponse(
            {
            "msg":"validation erorr",
            "error":data.get("error").popitem()[1]
                              },
                              status=400
            )
    try:
        with transaction.atomic():
            student, created = Student.objects.get_or_create(name=data.get("name"))
    except Exception:
        JsonResponse(
            {
                "msg":"student with name already exist"

            },
            status=400
        )
    
    student_q = Marks.objects.filter(subject=data.get("subject"),student=student)
    
    if student_q.exists():
        student_q.update(marks_obtained=F('marks_obtained') + data.get("mark"))
        
        return JsonResponse({"status":"success","operation":"update"})
    try:
        stuendt_objec = Student.objects.get(name=data.get("name"))
    except Exception:
        return JsonResponse({"status":"failed"})
    Marks.objects.create(subject=data.get("subject"),marks_obtained=data.get("mark"),student=stuendt_objec,classroom=stuendt_objec.current_classroom,date=timezone.now())
    
    return JsonResponse({"status":"success","operation":"create"})
