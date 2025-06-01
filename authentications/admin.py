from django.contrib import admin
from .models import Teacher,Student,Standard,ClassRoom,Marks
# Register your models here.
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Standard)
admin.site.register(ClassRoom)
admin.site.register(Marks)