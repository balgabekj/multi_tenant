from django.contrib import admin
from .models import BlogPost, Comment, Message, Notification
admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(Message)
admin.site.register(Notification)
