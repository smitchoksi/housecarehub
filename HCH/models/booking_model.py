from django.db import models
from .user_model import User
from .service_model import Service
from datetime import date, timedelta

class Booking(models.Model):
    name = models.CharField(max_length=256)
    contactno = models.BigIntegerField()
    address = models.TextField()
    area = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    booking_date_time = models.DateTimeField()
    booking_provide_date = models.DateField()
    booking_provide_time = models.CharField(max_length=20)
    booking_status = models.CharField(max_length=30)
    cancelledtime = models.DateTimeField(null=True,blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    service_id = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        b_id = str(self.id)
        return b_id

    #View Function
    @staticmethod
    def fetchdates():
        today = date.today()
        tomorrow = today + timedelta(days=1)
        previousday = tomorrow + timedelta(days=1)
        previousday_plus_one = previousday + timedelta(days=1)
        previousday_plus_two = previousday_plus_one + timedelta(days=1)

        # print("In fetchdates fun:",today)
        # today_d = str(today)
        # today_d = today_d[8:] + "-" + today_d[5:7] + "-" + today_d[0:4]
        #
        # tomorrow_d = str(tomorrow)
        # tomorrow_d = tomorrow_d[8:] + "-" + tomorrow_d[5:7] + "-" + tomorrow_d[0:4]
        #
        # previousday_d = str(previousday)
        # previousday_d = previousday_d[8:] + "-" + previousday_d[5:7] + "-" + previousday_d[0:4]
        #
        # previousday_plusone_d = str(previousday_plus_one)
        # previousday_plusone_d = previousday_plusone_d[8:] + "-" + previousday_plusone_d[5:7] + "-" + previousday_plusone_d[0:4]
        #
        #
        # previousday_plustwo_d = str(previousday_plus_two)
        # previousday_plustwo_d = previousday_plustwo_d[8:] + "-" + previousday_plustwo_d[5:7] + "-" + previousday_plustwo_d[0:4]


        dates = {
            'today': today,
            'tomrrow': tomorrow,
            'previousday': previousday,
            'previousday_plus_one': previousday_plus_one,
            'previousday_plus_two': previousday_plus_two
        }
        return dates

    @staticmethod
    def get_booking_by_uemail(email):
        try:
            return Booking.objects.filter(user_id=email)
        except:
            return False

    @staticmethod
    def get_booking_by_status(email,status):
        try:
            return Booking.objects.filter(user_id=email,booking_status=status)
        except:
            return False

    @staticmethod
    def get_bookings_by_booking_id(booking_id):
        try:
            return Booking.objects.get(id = booking_id)
        except:
            return False
