from django.contrib import admin
from .models import  Profile , HRDocument, ITDocument, SalesDocument, FinanceDocument, LogisticsDocument, PublicKey
from.models import SendDocument

# Register your models here.




admin.site.register(Profile)
admin.site.register(HRDocument)
admin.site.register(ITDocument)
admin.site.register(SalesDocument)
admin.site.register(FinanceDocument)
admin.site.register(LogisticsDocument)
admin.site.register(PublicKey)
admin.site.register(SendDocument)