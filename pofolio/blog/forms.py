# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person,BlogPost,Topic,Profile
from tinymce.widgets import TinyMCE

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(UserCreationForm):
    class Meta:
        model = Person
        fields = ['firstname', 'username', 'password1', 'password2','lastname']


# forms.py

class BlogPostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols': 80, 'rows': 30}))
    class Meta:
        model = BlogPost
        fields = ['topic','course','content','code','image']
        widgets = {
            'content': TinyMCE(attrs={'cols': 50, 'rows': 30},
                               mce_attrs={'content_style': 'body { background-color: auto; color: white; }'})
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text','content','image','code','course']
        
        
class Profileform(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['profile_pic']
