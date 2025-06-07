from django.db import models
from django.contrib.auth.models import User




class Standard(models.Model):
    name = models.CharField(max_length=100)  

    def __str__(self):
        return self.name


class ClassRoom(models.Model):
    standard = models.ForeignKey(Standard, on_delete=models.CASCADE)
    section = models.CharField(max_length=10) 
    academic_year = models.CharField(max_length=9)  

    def __str__(self):
        return f"{self.standard.name} - {self.section} ({self.academic_year})"


class Student(models.Model):
    name = models.CharField(
        max_length=100,
        null=True,blank=True,
        unique=True
                            )
    current_classroom = models.ForeignKey(ClassRoom, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
    


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    subject = models.CharField(max_length=100)
    assigned_classrooms = models.ManyToManyField(ClassRoom, blank=True) 

    def __str__(self):
        return self.user.username


class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True,blank=True)  
    subject = models.CharField(max_length=100)
    marks_obtained = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.student.user.username} - {self.subject} - "
