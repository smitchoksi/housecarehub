from django.db import models
from .sparepart_model import Sparepart
from .user_model import User
from .service_model import Service
from .booking_model import Booking
from .service_man_model import Serviceman
from .task_model import Task
from .updated_sparepart_model import Updated_Sparepart

class Sparepart_payment(models.Model):
    sparepart_amount = models.FloatField(default=0)
    sparepart_tax = models.FloatField()
    sparepart_total_amount = models.FloatField()
    updated_spareparts = models.ManyToManyField(Updated_Sparepart)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    task_id = models.ForeignKey(Task, on_delete=models.CASCADE)
    upi_id = models.CharField(max_length=50)