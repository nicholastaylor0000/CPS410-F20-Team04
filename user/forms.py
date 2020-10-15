from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, PassReset
from django.shortcuts import get_object_or_404


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError('Email addresses must be unique.')
        return super().clean()

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def clean(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')
        if email and User.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return super().clean()

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['qr_token']

class PasswordResetForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = PassReset
        fields = ['email']

    def is_valid(self):
        if valid := super().is_valid():
            email = self.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                self.instance.user = User.objects.get(email=email)
                return True

        return False
