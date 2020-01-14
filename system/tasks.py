from celery import shared_task
from check.maincheck import checkall

@shared_task
def main_check():
    checkall()
    return
