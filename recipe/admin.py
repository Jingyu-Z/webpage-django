from django.contrib import admin
from .models import Recipe
from .models import Category 
# Register your models here.


admin.site.register(Recipe)

admin.site.register(Category)