from django.contrib import admin
from django.urls import path
from .views import login_view,home_view,return_data_student,update_student,add_student_mark

urlpatterns = [
 path('login',login_view),
 path("home",home_view,name="home"),
 path('get-student-data/',return_data_student),
 path("update-student",update_student),
path("add-student",add_student_mark)

]

