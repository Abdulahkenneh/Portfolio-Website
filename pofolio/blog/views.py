from django.shortcuts import render
from django.http import HttpRequest,request
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, RegistrationForm,BlogPostForm,TopicForm
from .models import Topic,Courses,BlogPost,Person,Profile, UserTopicProgress
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import BlogPostForm, TopicForm
from django.urls import reverse
from .forms import RegistrationForm, LoginForm,Profileform
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone





links = {'links':{
        'linkdin':'https://hu.linkedin.com/in/abdulah-mamadee-kenneh-399023175',
        'facebook':'https://www.facebook.com/kennehabdulah1',
        'youtube':'https://www.youtube.com/channel/UCA70y0lJeIK3MKBj5xiUyew',
        'whatsapp':'https://wa.me/36206257091',
        }
               
           
           
        
        }


def index(request):
    topics = Topic.objects.all()
    search_query = request.GET.get('search')
    if search_query:
        # Search for topics based on the search query

        search_results = Topic.objects.filter(
        Q(text__icontains=search_query.strip()) |
        Q(text__icontains=search_query.replace(" ", "")) |
        Q(text__icontains=search_query.lower()) |
        Q(text__icontains=search_query.upper()) |
        Q(text__icontains=search_query.title()) |
        Q(content__icontains=search_query.strip()) |
        Q(content__icontains=search_query.replace(" ", "")) |
        Q(content__icontains=search_query.lower()) |
        Q(content__icontains=search_query.upper()) |
        Q(content__icontains=search_query.title())|
        Q(course__name__icontains=search_query.strip()) |
        Q(course__name__icontains=search_query.replace(" ", "")) |
        Q(course__name__icontains=search_query.lower()) |
        Q(course__name__icontains=search_query.upper()) |
        Q(course__name__icontains=search_query.title())
    ).distinct()
    else:
        search_results = None
   # courses = get_object_or_404(Courses,pk=course_id)
    contex={"topics":topics,'search_results':search_results,'search_value': search_query}  
    return render(request,"blog/home.html",contex)


def base_view(request):
    global links
    return render(request, "blog/base.html",links)

def pofolio_view(request):
    global links
    return render(request, "blog/pofolio.html",links)
  
def blog_view(request):
    #The function return the list of topic for all the topic in the Topic model 
    # Query the BlogPost objects associated with the retrieved user
    topics = Topic.objects.order_by('date_of_entry')
    blog_posts = BlogPost.objects.order_by('post_date')
    return render(request, "blog/myblog.html",context={'posts':blog_posts,'topics':topics})
# views.py



def blog_detail_view(request):
    return render(request,"blog/myblog.html")



def course_view(request):
    return render(request,template_name="blog/courses.html")
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:home')  # Redirect to the homepage after login
    else:
        form = LoginForm()
    return render(request, 'blog/login.html', {'form': form})





def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            firstname = form.cleaned_data.get('firstname')
            lastname = form.cleaned_data.get('lastname')
            # Creating a new Person instance and saving it to the database
            new_user = Person.objects.create_user(username=username, password=password, firstname=firstname, lastname=lastname)
            new_user.save()
            # Authenticating the new user and logging them in
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('blog:home')  # Redirect to your desired URL after successful registration
    else:
        form = RegistrationForm()
    return render(request, 'blog/register.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect( reverse('blog:home'))  # Redirect to the homepage after logout

@login_required(login_url="/login/")

def create_blogpost(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.user = request.user
            blog_post.save()
            return redirect('blog:home')  # Redirect after successful form submission
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_blogpost.html', {'form': form})

@login_required(login_url="/login/")
def create_topic(request):
    if request.method == 'POST':
        form = TopicForm(request.POST, request.FILES)
        if form.is_valid():
            form.user = request.user
            form.save()
            return redirect('blog:home')  # Redirect after successful form submission
    else:
        form = TopicForm()
    return render(request, 'blog/create_topic.html', {'form': form})

@login_required(login_url="/login/")
def all_topics(request):
    topics = Topic.objects.all().order_by('-date_of_entry')
    requested_topic = request.GET.get('search')
    #topics = Topic.objects.order_by('date_of_entry')
    courses = Courses.objects.all()
    posts = BlogPost.objects.order_by('post_date')
    contex ={"topics":topics,'courses':courses,'posts':posts}
    return render(request, 'blog/all_topic.html', context=contex)

@login_required(login_url="/login/")
def topic_detail(request, topic_id):
    topics= Topic.objects.order_by('date_of_entry')
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'blog/topic_detail.html', {'topic': topic,'topics':topics})


@login_required(login_url="/login/")

@login_required(login_url="/login/")
def mytopic_detail(request, topic_id):
    mytopic = get_object_or_404(Topic, pk=topic_id)
    
    
    # Track user's progress for this topic
    UserTopicProgress.objects.get_or_create(user=request.user, topic=mytopic, defaults={'date_accessed': timezone.now()})
    progress= UserTopicProgress.objects.all()
    context = {'mytopic': mytopic,'progress':progress}
    return render(request, 'blog/mytopic_detail.html', context=context)

@login_required(login_url="/login/")
def courses_detail(request,course_id):
    mycourse = get_object_or_404(Courses,pk=course_id)
    topics = Topic.objects.filter(course=mycourse).order_by('date_of_entry')
    
     # Retrieve the courses the user is registered for
    registered_courses = request.user.enroll_courses.all()
    
    # Dictionary to store course progress
    course_progress_dict = {}
    
    # Iterate through registered courses
    for course in registered_courses:
        # Retrieve topics related to the course
        topics = Topic.objects.filter(course=course).order_by('date_of_entry')
        
        # Retrieve the topics the user has accessed for this course
        user_topics = request.user.user_topic_progress.filter(topic__course=course)
        
        # Store course, related topics, and user's progress in the dictionary
        course_progress_dict[course] = {'topics': topics, 'user_topics': user_topics}
        
    contex={"course":mycourse,'topics':topics,'course_progress_dict': course_progress_dict}
        
    return render(request,template_name="blog/course_detail.html",context=contex)



def blogpost_detail_view(request, topic_id):
    # Retrieve the topic object based on the provided username
    topics = Topic.objects.order_by('date_of_entry')
    blogs = BlogPost.objects.order_by('post_date')
    # Query the BlogPost objects associated with the retrieved user
    blog_posts = get_object_or_404(BlogPost, pk=topic_id)
    context = {'post': blog_posts,'topics':topics,'blogs':blogs}
    return render(request, template_name='blog/blogpost_detail.html', context=context)



# Registering user for course

# views.py
@login_required(login_url="/login/")
def register_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    
    # Check if the user is already registered for the course
    if request.user in course.registered_users.all():
        messages.warning(request, 'You are already registered for this course.')
        return redirect('blog:profile')
    
    if request.method == 'POST':
        course.registered_users.add(request.user)
        messages.success(request, 'You have successfully registered for the course.')
        return redirect('blog:profile')
    
    return render(request, 'blog/register_course.html', {'course': course})




@login_required(login_url="/login/")
def profile_view(request):
    
    # Get the currently logged-in user
    mycourses = Courses.objects.filter(registered_users=request.user)
    #handling the profile form 
    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile')
    else:
        form = Profileform(instance=request.user)

    context={'mycourses':mycourses,'form':form}
    return render(request,template_name='blog/profile.html',context=context)


# the profileform view                 
def profilepic_view(request):
    if request.method == 'POST':
        form = Profileform(request.POST, request.FILES)
        if form.is_valid():
            # Set the user for the profile
            form.instance.user = request.user
            form.save()
            return redirect('blog:profile')
        else:
            print(form.errors)  # Print form errors to console
    else:
        form = Profileform()
           
    return render(request, 'blog/profilepic.html', {'form': form})


# Unregistering user from a course 

# views.py

@login_required(login_url="/login/")
def unregister_course(request, course_id):
    course = get_object_or_404(Courses, pk=course_id)
    
    # Check if the user is registered for the course
    if request.user in course.registered_users.all():
        course.registered_users.remove(request.user)
        messages.success(request, 'You have successfully unregistered from the course.')
    else:
        messages.warning(request, 'You are not registered for this course.')
    
    return redirect('blog:profile')



def course_delete_confirmation_view(request,course_id):
    course = get_object_or_404(Courses, pk=course_id)
    context={'course':course}   
    return render(request,template_name='blog/confirm.html',context=context)


def course_progress(request):
    # Retrieve the courses the user is registered for
    registered_courses = request.user.enroll_courses.all()
    
    # Dictionary to store course progress
    course_progress_dict = {}
    
    # Iterate through registered courses
    for course in registered_courses:
        # Retrieve topics related to the course
        topics = Topic.objects.filter(course=course).order_by('date_of_entry')
        
        # Retrieve the topics the user has accessed for this course
        user_topics = request.user.user_topic_progress.filter(topic__course=course)
        
        # Store course, related topics, and user's progress in the dictionary
        course_progress_dict[course] = {'topics': topics, 'user_topics': user_topics}
    
    context = {'course_progress_dict': course_progress_dict}
    return render(request, 'blog/course_progress.html', context=context)