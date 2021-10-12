from .models import Teacher
from django.contrib import admin

# Register your models here.
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('username','major')

admin.site.register(Teacher, TeacherAdmin)
