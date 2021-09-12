from django.contrib import admin

from .models import Folder, Document, Topic
# Register your models here.

admin.site.register(Topic)
admin.site.register(Folder)
admin.site.register(Document)
