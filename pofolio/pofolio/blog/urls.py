from django.urls import path

# urls.py
from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='home'),
    path('login/', views.login_view, name='login'),
    path('pofolio/', views.pofolio_view, name='pofolio'),
    path('progress/', views.course_progress, name='progress'),
    path('registers/<int:course_id>/', views.register_course, name='register_course'),
    path('unregister-course/<int:course_id>/', views.unregister_course, name='unregister_course'),
    path('confirm/<int:course_id>/', views.course_delete_confirmation_view, name='confirm'),
    path('blogs/', views.blog_view, name='blogs'),
    path('blogpost/<int:topic_id>/', views.blogpost_detail_view, name='blogpost_detail'),
    path('register/', views.register, name='register'),
    path('courses/',views.course_view,name="courses"),
    path("courses/<int:course_id>/",views.courses_detail,name="course_detail"),
    path("mytopic/<int:topic_id>/",views.mytopic_detail,name="mytopic_detail"),
    path('logout/', views.logout_view, name='logout'),
    path("topic/",views.create_topic,name="topic"),
    path("entry/",views.create_blogpost,name="entry"),
    path("profilepic/",views.profilepic_view,name="profilepic"),
    path("profile/", views.profile_view, name="profile"),
    path("topics",views.all_topics,name="topics"),
    path('topics/<int:topic_id>/', views.topic_detail, name='topic_detail'),
     # Other URL patterns...
]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)



app_name="blog"