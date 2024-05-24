from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.
User = get_user_model()

class Post(models.Model):
    user=models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE, null=True, blank=True)
    title=models.CharField(max_length=55)
    slug=models.SlugField(max_length=55)
    intro=models.CharField(max_length=55)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    image=models.ImageField(upload_to='uploads/', blank=True,null=True)
    likes = models.ManyToManyField(User, blank=True)
    shares=models.IntegerField(default=0)

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering=('-created_at',)


class Comment(models.Model):
    post=models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=255)
    email=models.EmailField()
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)

# posts.Post
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'post']


# class CustomUser(AbstractUser):
#     image=models.ImageField(upload_to='profile_pics', null=True, blank=True)