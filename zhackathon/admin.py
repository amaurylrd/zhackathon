from django.contrib import admin

from .models import Comment, Festival

# Register your models here.
admin.site.register(Festival)
admin.site.register(Comment)
