from django.contrib import admin
from .models import Company, Price, ScrapyItem, PredictedPrice
# Register your models here.
admin.site.register(Company)
admin.site.register(Price)
admin.site.register(PredictedPrice)
admin.site.register(ScrapyItem)
