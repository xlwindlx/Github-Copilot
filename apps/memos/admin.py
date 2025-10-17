from django.contrib import admin
from .models import Memo


@admin.register(Memo)
class MemoAdmin(admin.ModelAdmin):
	list_display = ("id", "title", "owner", "is_public", "updated_at")
	list_filter = ("is_public", "owner")
	search_fields = ("title", "body")

# Register your models here.
