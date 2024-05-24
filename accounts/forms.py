# from . models import CustomUser
from django import forms

from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['image']
