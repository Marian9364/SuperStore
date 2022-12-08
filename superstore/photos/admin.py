from django.contrib import admin

# Register your models here.
from superstore.photos.models import Toy


@admin.register(Toy)
class ToyAdmin(admin.ModelAdmin):
    list_display = ("toy_name", "slug")
