from django import forms
from .models import Comment
from django.contrib.auth import get_user_model

# Custom user import in below line
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body','post']


# User = get_user_model()
# class CustomUserForm(forms.ModelForm):
#     class Meta:
#         model=User
#         fields=['image']
