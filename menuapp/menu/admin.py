from django.contrib import admin
from menu import models


@admin.register(models.MenuModel)
class MenuAdmin(admin.ModelAdmin):
    pass