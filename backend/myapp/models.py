

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    usertype = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, null=True)


class Teacher(models.Model):
    teacher_id = models.ForeignKey(User, on_delete=models.CASCADE,null=True,blank=True)
    salary = models.IntegerField()
    experience = models.IntegerField()
    teacher_pic = models.ImageField(upload_to="media", null=True)
    is_approved = models.BooleanField(default=False)


class Student(models.Model):
    student_id = models.ForeignKey(User, on_delete=models.CASCADE)
    guardian = models.CharField(max_length=30)
    is_approved = models.BooleanField(default=False)

