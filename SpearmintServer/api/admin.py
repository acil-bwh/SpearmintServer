from django.contrib import admin
from SpearmintServer.api.models import QueueItem
# Register your models here.


class QueueItemAdmin(admin.ModelAdmin):
    pass

admin.site.register(QueueItem,QueueItemAdmin)