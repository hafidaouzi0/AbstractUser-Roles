from django.db import models
from django.contrib.auth.models import AbstractUser
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
        

    