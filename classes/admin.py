from django.contrib import admin

from .models import YogaClass


class YogaClassAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(YogaClass, YogaClassAdmin)
