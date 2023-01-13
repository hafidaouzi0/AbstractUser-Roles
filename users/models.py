from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
# Create your models here.

class User(AbstractUser):
      class role_user(models.TextChoices):
         ADMIN="ADMIN",'Admin'#'ADMIN': will be stored in the databse and 'Admin' will be readable human being
         STUDENT="STUDENT",'Student'
         TEACHER="TEACHER",'Teacher'
 
      base_role_user=role_user.ADMIN

      Role=models.CharField(max_length=60,choices=role_user.choices)

      def save(self,*args,**kwargs):
        #id the user doesn't have a pk : means if the user hasn't being created
        if not self.pk:
            self.Role=self.base_role_user
        return super().save(*args,**kwargs)

#A Manager is the interface through which database query operations are provided to Django models.
#  At least one Manager exists for every model in a Django application.
class StudentManager(BaseUserManager):
    def get_queryset(self,*args,**kwargs):
        results=super().get_queryset(*args,**kwargs)
        return results.filter(Role=User.role_user.STUDENT)

#a proxy model that inhirets from the Abstractuser won't get anpther table in the db 
class Student(User):

    base_role_user= User.role_user.STUDENT

    student=StudentManager()
    
    class Meta:
        proxy=True
    
    def welcome(self):
        return  "only for students"





#Teacher Manager

class TeacherManager(BaseUserManager):

    def get_queryset(self,*args,**kwargs):
        results=super().get_queryset(*args,**kwargs)
        return results.filter(Role=User.role_user.TEACHER)




#Teacher model

class Teacher(User):

    base_role_user=User.role_user.TEACHER
    teacher=TeacherManager()

    class Meta:
        proxy=True
    
    def welcome(self):
        return "only for teachers"
        

    