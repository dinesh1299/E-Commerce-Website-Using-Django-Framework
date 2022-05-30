from dataclasses import fields
from pyexpat import model
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Customer

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit

class CreateUserForm(UserCreationForm):
    class Meta:
        model=User
        fields=[
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
            
        ]

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=[
            'name',
            'mobile',
            'email',
            'address'
        ]
