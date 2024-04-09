from django.contrib import admin
from .models import  Profile , HRDocument, ITDocument, SalesDocument

# Register your models here.




admin.site.register(Profile)
admin.site.register(HRDocument)
admin.site.register(ITDocument)
admin.site.register(SalesDocument)
