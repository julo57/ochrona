from django.forms import ModelForm
from .models import Profile , HRDocument, SalesDocument, ITDocument ,Document, FinanceDocument, LogisticsDocument, PublicKey,SendKey
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
import os
import re
from .models import SendDocument

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
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
        ('FINANCE', 'FINANCE'),
        ('LOGISTICS', 'LOGISTICS'),
    )
    folder = forms.ChoiceField(choices=FOLDER_CHOICES, required=False)
    recipient = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        label="Recipient",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    public_key = forms.ModelChoiceField(
        queryset=PublicKey.objects.none(),  # Initially empty, will be set dynamically
        label="Public Key",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Select the public key to include with the document.",
        required=True
    )

    class Meta:
        model = Document  # This should be a concrete model if not abstract
        fields = ('title', 'file', 'recipient', 'public_key', 'folder')

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(DocumentForm, self).__init__(*args, **kwargs)

        department_document_class = {
            'IT': ITDocument,
            'Sales': SalesDocument,
            'HR': HRDocument,
            'FINANCE': FinanceDocument,
            'LOGISTICS': LogisticsDocument
        }
        document_class = department_document_class.get(user_profile.department, Document)
        self.instance.__class__ = document_class
        self._meta.model = document_class  # Dynamically change the form model

        if not hasattr(document_class, 'folder'):
            self.fields.pop('folder', None)

        if user_profile:
            self.fields['public_key'].queryset = PublicKey.objects.filter(profile=user_profile)

class UserRoleForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['role', 'department']

class SendKeyForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        label="Recipient",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    public_key = forms.ModelChoiceField(
        queryset=PublicKey.objects.none(),
        label="Public Key",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = SendKey
        fields = ['recipient', 'public_key']

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(SendKeyForm, self).__init__(*args, **kwargs)
        if user_profile:
            self.fields['public_key'].queryset = PublicKey.objects.filter(profile=user_profile)

class SendDocumentForm(forms.ModelForm):
    DEPARTMENT_CHOICES = (
        ('HR', 'HR'),
        ('Sales', 'Sales'),
        ('IT', 'IT'),
        ('FINANCE', 'Finance'),
        ('LOGISTICS', 'Logistics')
    )

    department = forms.ChoiceField(
        choices=DEPARTMENT_CHOICES,
        label="Department",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False  # Make department optional
    )
    recipient = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        label="Recipient",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    recipients = forms.ModelMultipleChoiceField(
        queryset=Profile.objects.all(),
        label="Additional Recipients",
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        required=False
    )
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        required=True
    )
    file = forms.FileField(
        label="Document File",
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        required=True
    )
    is_public = forms.BooleanField(
        label="Is Public",
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    
    class Meta:
        model = SendDocument
        fields = ('title', 'file', 'department', 'recipient', 'recipients', 'is_public')

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(SendDocumentForm, self).__init__(*args, **kwargs)

class PublicKeyForm(forms.ModelForm):
    class Meta:
        model = PublicKey
        fields = ['key']

    def __init__(self, *args, profile=None, **kwargs):
        super(PublicKeyForm, self).__init__(*args, **kwargs)
        self.profile = profile

    def save(self, commit=True):
        instance = super(PublicKeyForm, self).save(commit=False)
        instance.profile = self.profile
        if commit:
            instance.save()
        return instance

class SendKeyForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        label="Recipient",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    public_key = forms.ModelChoiceField(
        queryset=PublicKey.objects.none(),
        label="Public Key",
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    class Meta:
        model = SendKey
        fields = ['recipient', 'public_key']

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(SendKeyForm, self).__init__(*args, **kwargs)
        if user_profile:
            self.fields['public_key'].queryset = PublicKey.objects.filter(profile=user_profile)

    