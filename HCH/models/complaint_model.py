from django.db import models
from django.utils.safestring import mark_safe
from .user_model import User
from .booking_model import Booking
from .service_model import Service

complaint_status_choice = [
    ("1", "Pending"),
    ("2", "solved")
]
class Complaint(models.Model):
    complaint_date = models.DateTimeField()
    complaint_topic = models.CharField(max_length=100)
    complaint_pic = models.ImageField(upload_to='complaints')
    complaint_description = models.TextField()
    complaint_status = models.CharField(default="Pending", max_length=30)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    booking_id = models.ForeignKey(Booking, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)

    def complaint_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.complaint_pic.url))

    complaint_photo.allow_tags = True