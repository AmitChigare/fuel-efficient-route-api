from django.contrib import admin
from .models import School


# Register your models here.
class SchoolAdmin(admin.ModelAdmin):
    list_display = ["name", "pin_code", "latitude", "longitude"]


admin.site.register(School, SchoolAdmin)
