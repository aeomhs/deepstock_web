from django.contrib import admin
from .models import Company, Price, ScrapyItem
# Register your models here.
admin.site.register(Company)
admin.site.register(Price)
admin.site.register(ScrapyItem)