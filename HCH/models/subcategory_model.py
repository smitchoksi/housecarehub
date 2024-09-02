from django.db import models
from django.utils.safestring import mark_safe
from .category_model import Category
class Subcategory(models.Model):
    subcatname = models.CharField(max_length=256)
    subcatimage = models.ImageField(upload_to='subcategory')
    catname = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.subcatname
    def subcategory_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.subcatimage.url))

    subcategory_photo.allow_tags = True

    #Views function
    @staticmethod
    def get_subcategory_of_category(cat_id):
        return Subcategory.objects.filter(catname=cat_id)