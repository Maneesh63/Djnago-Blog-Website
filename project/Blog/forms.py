
from typing import Any
from .models import CustomUser,Post,likes,UserProfile,Comment
from django.contrib.auth.forms import UserCreationForm

from django.core.exceptions import ValidationError

from django import forms


class Userform(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email']

    #function to remove the Default help instruction given by Django Forms 
    def __init__(self,*args, **kwargs):
          super().__init__(*args,**kwargs)
          self.fields['password1'].help_text = None
          self.fields['password2'].help_text = None

          #To remove the confirm password field
          del self.fields['password2'] 
    
    

class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class postform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','description','image']
       
        

class Updatepostform(forms.ModelForm):
    class Meta:
        model=Post
        fields=['title','description','image']


# forms.py
 

class SearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False)



class likeform(forms.ModelForm):
    class Meta:
         model=likes
         fields = ['user', 'post']
         widgets = {'user': forms.HiddenInput()}


 
  

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio','image']  

class Edituserform(forms.ModelForm):
    class Meta :
        model= CustomUser
        fields=['username','email']


class Commentform(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['comment']
