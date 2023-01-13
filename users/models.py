from django.db import models
from django.contrib.auth.models import (AbstractUser,BaseUserManager)
# Create your models here.

class User(AbstractUser):
      class Role(models.TextChoices):
         ADMIN="ADMIN",'Admin'#'ADMIN': will be stored in the databse and 'Admin' will be readable human being
         STUDENT="STUDENT",'Student'
         TEACHER="TEACHER",'Teacher'
 
      base_role=Role.ADMIN

      Role=models.CharField(max_length=60,choices=Role.choices)

      def save(self,*args,**kwargs):
        #id the user doesn't have a pk : means if the user hasn't being created
        if not self.pk:
            self.role=self.base_role
        return super().save(*args,**kwargs)

#A Manager is the interface through which database query operations are provided to Django models.
#  At least one Manager exists for every model in a Django application.
class StudentManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        results=super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.STUDENT)

#a proxy model that inhirets from the Abstractuser won't get anpther table in the db 
class Student(User):
    base_role=User.Role.STUDENT
    student=StudentManager()
    class Meta:
        proxy=True
    
    def welcome(self):
        return  "only for students"



#Teacher Manager

class TeacherManager(BaseUserManager):

    def get_queryset(self,*args,**kwargs):
        results=super().get_queryset(*args,**kwargs)
        return results.filter(role=User.Role.TEACHER)




#Teacher model

class Teacher(User):

    base_role=User.Role.TEACHER
    teacher=TeacherManager()

    class Meta:
        proxy=True
    
    def welcome(self):
        return "only for teachers"
        

    