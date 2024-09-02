from django.db import models
from HCH.models.task_model import Task
from HCH.models.sparepart_model import Sparepart

class Updated_Sparepart(models.Model):
    task_id = models.ForeignKey(Task,on_delete=models.CASCADE)
    # sparepart_ids = models.ManyToManyField(Sparepart)
    sparepart_id = models.ForeignKey(Sparepart,on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True,blank=True)
    square_feet = models.IntegerField(null=True, blank=True)