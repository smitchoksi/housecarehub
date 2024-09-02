from django.db import models
from .user_model import User
from .booking_model import Booking
from .service_model import Service

class Feedback_rating(models.Model):
    rating = models.IntegerField()
    feedback_title = models.CharField(max_length=100)
    feedback_description = models.TextField()
    feedback_datetime = models.DateTimeField()
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)