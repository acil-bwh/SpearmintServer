from .models import QueueItem

def enqueue():
    item = QueueItem.objects.create()
    return item.id

def peek(job_id, upto_first_n=1):
    # check if job_id is one of the first N items from the head of queue
    top_items = QueueItem.objects.order_by('pk')[:upto_first_n]
    for item in top_items:
        if job_id == item.id:
            return True
    return False

def dequeue(job_id):
    QueueItem.objects.get(pk=job_id).delete()
