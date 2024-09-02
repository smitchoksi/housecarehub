from django.db import models
from .sparepart_title_model import Spareparttitle

class Sparepart(models.Model):
    sparepart_title = models.ForeignKey(Spareparttitle, on_delete=models.CASCADE)
    sparepart_name = models.CharField(max_length=100)
    sparepart_price = models.IntegerField()
    sparepart_quantity = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return self.sparepart_name