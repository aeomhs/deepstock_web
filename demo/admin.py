from django.contrib import admin
from .models import Company, PredictedPrice
# Register your models here.
admin.site.register(Company)
admin.site.register(PredictedPrice)
