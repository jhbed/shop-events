from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
    '''
    By default, the UserCreationForm class only includes username, pass1, pass2. 
    We need to add some fields to this form, as done belo
    '''

    email = forms.EmailField(required=True) #required by default, specifying for clarity

    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']

class UserUpdateForm(forms.ModelForm):

    email = forms.EmailField(required=True) #required by default, specifying for clarity

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['image']


    
