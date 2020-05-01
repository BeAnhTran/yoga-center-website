from django.contrib import admin

from .models import Course


class CourseAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Course, CourseAdmin)
