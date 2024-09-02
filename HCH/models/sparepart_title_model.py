from django.db import models
from .category_model import Category
from .subcategory_model import Subcategory

class Spareparttitle(models.Model):
    sp_title = models.CharField(max_length=256)
    sp_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sp_subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.sp_title