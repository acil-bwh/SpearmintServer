from django.db import models

class QueueItem(models.Model):
    ITEM_TYPE_CHOICES = (
        ('s', 'Suggest'),
        ('u', 'Update'),
    )
    item_type = models.CharField(max_length=1, choices=ITEM_TYPE_CHOICES, default='s')
    timestamp = models.DateTimeField(auto_now=True)
