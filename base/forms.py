from django.forms import ModelForm
from .models import Profile , HRDocument, SalesDocument, ITDocument 
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import re

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class ProfileForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), label="Password", min_length=8)
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label="Confirm Password")
    

    class Meta:
        model = Profile
        fields = ['username', 'email', 'password']


    def clean_email(self):
        email = self.cleaned_data.get("email")
        email_regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
        if not email_regex.match(email):
            raise ValidationError("Invalid email format.")
        if Profile.objects.filter(email=email).exists():
            raise ValidationError("Email already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error('confirm_password', "Passwords do not match.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class DocumentForm(forms.ModelForm):
    FOLDER_CHOICES = (
        ('IT', 'IT'),
        ('Sales', 'Sales'),
        ('HR', 'HR'),
    )
    folder = forms.ChoiceField(choices=FOLDER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(DocumentForm, self).__init__(*args, **kwargs)
        
        # Usuń pole 'folder', jeśli model nie ma tego pola
        if not hasattr(HRDocument, 'folder'):
            del self.fields['folder']


class UserRoleForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['role', 'department']
