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
    def save(self, commit=True):
        user = super(UpdateUserForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class UpdateAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["avatar", "last_edit"]
