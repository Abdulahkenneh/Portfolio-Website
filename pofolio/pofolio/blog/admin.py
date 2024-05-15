from django.contrib import admin
from .models import Person,BlogPost,Courses,Topic,Profile,UserTopicProgress
from tinymce.widgets import TinyMCE
from .forms import BlogPostForm

# Register your models here.
admin.site.register(Person)
#admin.site.register(BlogPost)
from django.db import models
admin.site.register(Courses)
admin.site.register(Topic)
admin.site.register(Profile)
admin.site.register(UserTopicProgress)

#class Blogpost(admin.ModelAdmin):
  #  pass

class ModelBlogpost(admin.ModelAdmin):
    form = BlogPostForm

admin.site.register(BlogPost, ModelBlogpost)
