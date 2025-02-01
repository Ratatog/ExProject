from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class RegisterUserForm(UserCreationForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput())
    password2 = forms.CharField(label='confirm', widget=forms.PasswordInput())
    
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='username')
    password = forms.CharField(label='password')
    
    class Meta:
        model = get_user_model
        fields = ['username', 'password']