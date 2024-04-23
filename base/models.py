from django.db import models
from django.utils import timezone
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
    password = models.CharField(max_length=128)  # W prawdziwych projektach użyj Django auth system
    role = models.CharField(max_length=20, choices=USER_ROLES, default='guest')
    department = models.CharField(max_length=100, choices=USER_DEPARTMENT, default='HR')

    def __str__(self):
        return self.username

class Document(models.Model):
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')  # Będziemy modyfikować tę ścieżkę w widoku
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
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
