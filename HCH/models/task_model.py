from django.db import models
from HCH.models.booking_model import Booking
from HCH.models.service_man_model import Serviceman

class Task(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    serviceman_id = models.ForeignKey(Serviceman,on_delete=models.CASCADE,null=True,blank=True)
    status = models.CharField(default="Pending",max_length=20)    #Pending, Allocated,Completed
    assign_time = models.DateTimeField(null=True,blank=True)
    pick_time = models.DateTimeField(null=True,blank=True)
    start_time = models.DateTimeField(null=True,blank=True)
    complete_time = models.DateTimeField(null=True,blank=True)
    close_task = models.DateTimeField(null=True,blank=True)
    need_sparepart = models.BooleanField(default=False)
    # other = models.TextField(null=True,blank=True)

    #status = Pending, Allocated, Picked, Start Work, Completed, Closed, Cancelled
    @staticmethod
    def get_task_by_task_id(task_id):
        try:
            return Task.objects.get(id=task_id)
        except:
            return False



    @staticmethod
    def get_pending_task():
        try:
            return Task.objects.filter(status="Pending")
        except:
            return False

    @staticmethod
    def get_allocated_task():
        try:
            return Task.objects.filter(status="Allocated")
        except:
            return False

    @staticmethod
    def get_picked_task():
        try:
            return Task.objects.filter(status="Picked")
        except:
            False

    @staticmethod
    def get_completed_task():
        try:
            return Task.objects.filter(status="Completed")
        except:
            return False

    @staticmethod
    def get_cancelled_task():
        try:
            return Task.objects.filter(status="Cancelled")
        except:
            return False