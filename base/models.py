from django.db import models

from django.core.validators import FileExtensionValidator
from django.utils import timezone
from datetime import timedelta

class Profile(models.Model):
    USER_ROLES = (
        ('superadmin', 'Super Administrator'),
        ('admin', 'Administrator'),
        ('manager', 'Manager'),
        ('employee', 'Pracownik'),
        ('guest', 'Gość'),
    )

    USER_DEPARTMENT = (
        ('HR', 'HR'),
        ('IT', 'IT'),
        ('SALES', 'SALES'),
        ('FINANCE', 'FINANCE'),
        ('LOGISTICS', 'LOGISTICS'),
    )

    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  
    role = models.CharField(max_length=20, choices=USER_ROLES, default='guest')
    department = models.CharField(max_length=100, choices=USER_DEPARTMENT, default='HR')
    login_attempts = models.IntegerField(default=0)
    lockout_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    def is_locked_out(self):
        if self.lockout_time and timezone.now() < self.lockout_time:
            return True
        return False

    def increment_login_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 3:
            self.lockout_time = timezone.now() + timedelta(minutes=5)
            self.login_attempts = 0
        self.save()

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.lockout_time = None
        self.save()

class PublicKey(models.Model):
    key = models.TextField()  # Zaszyfrowany klucz publiczny
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='public_keys')
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'{self.profile.username} - {self.key[:10]}...'  # Only show part of the key for readability
class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['gpg'])]
    ) 
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=False)
    public_key = models.ForeignKey(PublicKey, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        abstract = True


    def __str__(self):
        return self.title

class HRDocument(Document):
    last_edited_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='hrdocument_last_edited')
    last_replaced_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='hrdocument_last_replaced')
    last_replaced_at = models.DateTimeField(null=True, blank=True)
    recipient = models.ForeignKey(Profile, related_name='received_documents_HR', on_delete=models.SET_NULL, null=True, blank=True)


class ITDocument(Document):
    last_edited_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='itdocument_last_edited')
    last_replaced_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='itdocument_last_replaced')
    last_replaced_at = models.DateTimeField(null=True, blank=True)
    recipient = models.ForeignKey(Profile, related_name='received_documents_IT', on_delete=models.SET_NULL, null=True, blank=True)

class SalesDocument(Document):
    last_edited_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='salesdocument_last_edited')
    last_replaced_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='salesdocument_last_replaced')
    last_replaced_at = models.DateTimeField(null=True, blank=True)
    recipient = models.ForeignKey(Profile, related_name='received_documents_SALES', on_delete=models.SET_NULL, null=True, blank=True)

class FinanceDocument(Document):
    last_edited_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='financedocument_last_edited')
    last_replaced_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='financedocument_last_replaced')
    last_replaced_at = models.DateTimeField(null=True, blank=True)
    recipient = models.ForeignKey(Profile, related_name='received_documents_FINANCE', on_delete=models.SET_NULL, null=True, blank=True)


class LogisticsDocument(Document):
    last_edited_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='logisticsdocument_last_edited')
    last_replaced_by = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='logisticsdocument_last_replaced')
    last_replaced_at = models.DateTimeField(null=True, blank=True)
    recipient = models.ForeignKey(Profile, related_name='received_documents_LOGISTIC', on_delete=models.SET_NULL, null=True, blank=True)

class SendKey(models.Model):
    public_key = models.ForeignKey(PublicKey, on_delete=models.CASCADE)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_keys')
    recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_keys')
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Key from {self.sender.username} to {self.recipient.username}'

class SendDocument(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='documents/',
        validators=[FileExtensionValidator(allowed_extensions=['gpg'])]
    )
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    recipient = models.ForeignKey(Profile, related_name='received_single_documents', on_delete=models.SET_NULL, null=True, blank=True)
    recipients = models.ManyToManyField(Profile, related_name='received_documents', blank=True)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.title




