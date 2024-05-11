from django_quill.fields import QuillField
from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager,User
from django.db import models
from django.contrib.auth.models import User
from tinymce import models as tinymce_models
from django.conf import settings


class PersonManager(BaseUserManager):
    def create_user(self, username, password=None,**extra_fields):
        if not username:
            raise ValueError('The Username field must be set')

        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password,**extra_fields):
        user = self.create_user(username=username, password=password)
        user.is_superuser = True
        user.is_staff = True
        user.is_active =True
        user.save(using=self._db)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
    
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
    
        return user
    


class Person(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=150, unique=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to='images', height_field=None, width_field=None,blank=True)
    enroll_courses = models.ManyToManyField('Courses', related_name='students', blank=True)
    objects = PersonManager()
    USERNAME_FIELD = 'username'
    is_staff = models.BooleanField(default=False)
    
    
   
    def __str__(self):
            return self.username
    
    

class Courses(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=None,blank=True)
    discritption = models.CharField(max_length=100,default='') 
    date = models.DateTimeField(auto_now_add=True)
    registered_users = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)
    def __str__(self):
        return self.name


class Topic(models.Model):
    course = models.ForeignKey(Courses,on_delete=models.CASCADE)
    text= models.CharField(max_length=100)
    content = tinymce_models.HTMLField(blank=False,null=False)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=None,null=False,blank=True)
    code = tinymce_models.HTMLField(blank=True,null=False)
    date_of_entry = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f' {self.text} created  on {self.date_of_entry}'



class BlogPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
    topic = models.CharField(max_length=100)
    post_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=None,null=False,blank=True)
 
    course = models.ForeignKey(Courses, on_delete=models.CASCADE)
    code = tinymce_models.HTMLField(blank=False)
    content = tinymce_models.HTMLField()

    def __str__(self):
        return f"{self.user}'s Post on {self.post_date} in {self.course}"



class Profile(models.Model):
     user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True)
     image = models.ImageField(upload_to='images', height_field=None, width_field=None, max_length=None)
     
     def __str__(self):
         return (f'{self.user} image')
     
class UserTopicProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    date_accessed = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'topic')