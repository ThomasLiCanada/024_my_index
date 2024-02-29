# websites/admin.py

from django.contrib import admin
from .models import *


class IndexCategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_order_num',)


class IndexAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Index._meta.get_fields()]


class ToDoTaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ToDoTask._meta.get_fields()]


admin.site.register(IndexCategory, IndexCategoryAdmin)
admin.site.register(Index, IndexAdmin)
admin.site.register(ToDoTask, ToDoTaskAdmin)
