from django.db import models
from django.contrib.auth.models import User

class Tag(models.Model):
    tag_name = models.CharField(max_length=20)

class Image(models.Model):
    # blank = True is to disable the validation on the foreign key fields for required checking
    image_file = models.ImageField(upload_to='uploads/',null=True, blank=True)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_name = models.TextField()
    image_desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edit = models.DateTimeField(auto_now=True)

# last_edit is used to store the last edit time of the avatar and user related info
class Profile(models.Model):
    avatar = models.ImageField(upload_to='profile/',null=True, blank=True, default='noavatar.jpg')
    last_edit = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Activity(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
