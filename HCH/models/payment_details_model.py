from django.db import models
from .booking_model import Booking
from .service_model import Service
from .user_model import User

class Paymentdetails(models.Model):
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    upi_id = models.CharField(max_length=50)
    amount = models.IntegerField()
    tax = models.FloatField()
    totalamount = models.FloatField()
