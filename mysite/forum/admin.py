from django.contrib import admin

from .models import Topic, Message, Tag, Comment

# Register your models here.

admin.site.register(Topic)
admin.site.register(Message)
admin.site.register(Tag)
admin.site.register(Comment)