from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
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

#Students and teachers require separate profile data
#we gonna use post-save signal so that whenever we save a new user we gonna send a signal
#and capture that signal so that we can perform some additional task
#we gonna need the receiver to receive those signals

@receiver(post_save,sender=Student)
def create_user_profile(sender,instance,created,**kwargs):
    if created and instance.Role == "STUDENT":
        StudentProfile.objects.create(user=instance)




#Student profile
class StudentProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    student_id=models.IntegerField(null=True,blank=True)





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
        
@receiver(post_save,sender=Teacher)
def create_user_profile(sender,instance,created,**kwargs):
    if created and instance.Role == "TEACHER":
        Student.objects.create(user=instance)


    #Teacher profile 
class TeacherProfile(models.Model):
        user = models.OneToOneField(User,on_delete=models.CASCADE)
        teacher_id =models.IntegerField(null=True,blank=True)



    #test in terminal :use ctrl+/ to comment multiple lines
#     python manage.py shell

# >>> from users.models import Student,Teacher
# >>> Student.objects.create_user(username="safia",password="1234")
# <Student: safia>
# >>> Student.student.all() 
# <QuerySet [<Student: safia>]>
# >>> Teacher.objects.create_user(username="prof",password="1223")
# <Teacher: prof>
# >>> Teacher.teacher.all()
# <QuerySet [<Teacher: prof>]>
# >>> Teacher.objects.all() 
# <QuerySet [<Teacher: hafida>, <Teacher: safia>, <Teacher: prof>]>
# >>>



# the @receiver(post_save, sender=Student) is a decorator that registers a function create_user_profile as a signal receiver for the post_save signal emitted by the Student model. This means that the function create_user_profile will be called every time an instance of the Student model is saved.

# The create_user_profile function has four arguments: sender, instance, created, and **kwargs.

# sender is the model class that emitted the signal (in this case, the Student class).
# instance is the instance of the model that was saved.
# created is a boolean value that indicates whether the instance was just created or updated.
# **kwargs is a catch-all for any additional keyword arguments passed to the signal.
# In this function, the if statement checks if the instance is just created and has a role of "STUDENT". If both conditions are met, it creates a new StudentProfile instance and assigns the user attribute to the instance of the Student model that was just saved.

# The StudentProfile model has two fields:

# user field which has a one-to-one relationship with the User model, this means that for each User model, there will be one and only one StudentProfile model associated with it.
# student_id field which is an integer field that can be null and blank, this field can be used to store an additional information about the student.
# The post_save signal is emitted every time the save() method is called on an instance of the Student model. In this case, the create_user_profile function is called after the save() method is called on an instance of the Student model, this allows the developer to perform additional actions after the instance is saved.