from django.forms import ModelForm
from .models import Profile , HRDocument, SalesDocument, ITDocument ,Document, FinanceDocument, LogisticsDocument
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
        ('FINANCE', 'FINANCE'),
        ('LOGISTICS', 'LOGISTICS'),
    )
    folder = forms.ChoiceField(choices=FOLDER_CHOICES, required=False)

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(DocumentForm, self).__init__(*args, **kwargs)

        if user_profile:
            department_document_class = {
                'IT': ITDocument,
                'Sales': SalesDocument,
                'HR': HRDocument,
                'FINANCE': FinanceDocument,
                'LOGISTICS': LogisticsDocument
            }
            document_class = department_document_class.get(user_profile.department, Document)
            self.instance.__class__ = document_class
            self._meta.model = document_class  # zmieniamy model formularza dynamicznie
            
            # Usuń pole 'folder', jeśli model nie ma tego pola
            if not hasattr(document_class, 'folder'):
                self.fields.pop('folder', None)


class UserRoleForm(forms.ModelForm):
    
    class Meta:
        model = Profile
        fields = ['role', 'department']

class SendDocumentForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=Profile.objects.all(),
        label="Recipient",
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Document  # Ustaw ogólny model Document jeżeli jest nieabstrakcyjny, w przeciwnym razie ustal poniżej
        fields = ('recipient',)  # Możesz dodać tu więcej pól zależnie od potrzeb

    def __init__(self, *args, **kwargs):
        user_profile = kwargs.pop('user_profile', None)
        super(SendDocumentForm, self).__init__(*args, **kwargs)

        # Zależnie od departamentu ustaw odpowiedni model dokumentów
        department_documents = {
            'HR': HRDocument.objects.all(),
            'IT': ITDocument.objects.all(),
            'SALES': SalesDocument.objects.all(),
            'FINANCE': FinanceDocument.objects.all(),
            'LOGISTICS': LogisticsDocument.objects.all(),
        }

        # Ustaw queryset dla dokumentów zgodnie z departamentem profilu użytkownika
        if user_profile and user_profile.department in department_documents:
            self.fields['document'] = forms.ModelChoiceField(
                queryset=department_documents[user_profile.department],
                label="Select Document",
                widget=forms.Select(attrs={'class': 'form-control'})
            )
        else:
            # Jeżeli profil nie ma przypisanego departamentu, nie pokazuj dokumentów
            self.fields['document'] = forms.ModelChoiceField(
                queryset=Document.objects.none(),  # Zakładając, że Document nie jest abstrakcyjny
                label="Select Document",
                widget=forms.Select(attrs={'class': 'form-control'})
            )