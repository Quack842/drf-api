from django.contrib import admin
from .models import Profile
from comments.models import Comment

admin.site.register(Profile)
admin.site.register(Comment)
