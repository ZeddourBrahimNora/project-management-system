from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from blog.models import Task
from .models import Profile

class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField()
    
    class Meta :
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
        
class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
    
    class Meta :
        model = User
        fields = ['username', 'email']
        
        
class ProfileUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['image']


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'assigned_to']

