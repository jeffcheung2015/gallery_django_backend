from django import forms
from .models import Image, Profile
from django.contrib.auth.models import User
from django.db import models

class UpsertImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ["image_name", "image_desc", "image_file", "user", "tags"]

class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password"]


class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "last_edit"]
