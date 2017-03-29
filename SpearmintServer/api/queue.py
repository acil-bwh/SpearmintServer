from .models import QueueItem

def enqueue(queue_type='s'):
    item = QueueItem.objects.create(item_type=queue_type)
    return item.id

def peek(queue_type,queue_id, upto_first_n=1):
    # check if job_id is one of the first N items from the head of queue
    top_items = QueueItem.objects.filter(item_type=queue_type).order_by('pk')[:upto_first_n]
    for item in top_items:
        if queue_id == item.id:
            return True
    return False

def dequeue(queue_id):
    QueueItem.objects.get(pk=queue_id).delete()
