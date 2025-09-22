from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "is_completed", "created_at")
    list_filter = ("is_completed", "owner")
    search_fields = ("title", "description")
