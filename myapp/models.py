from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    usertype=models.CharField(max_length=50)

class Department(models.Model):
    department_name=models.CharField(max_length=50)

class Student1(models.Model):
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    stud_id=models.ForeignKey(User,on_delete=models.CASCADE)
    age=models.IntegerField()
    phone=models.BigIntegerField()
    class Meta:
        db_table='Student1'

class Teacher1(models.Model):
    department_id=models.ForeignKey(Department,on_delete=models.CASCADE)
    teach_id=models.ForeignKey(User,on_delete=models.CASCADE)
    age=models.IntegerField()
    phone=models.BigIntegerField()
    class Meta:
        db_table='Teacher1'
