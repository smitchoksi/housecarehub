from django.db import models
from django.utils.safestring import mark_safe
from .category_model import Category
from .subcategory_model import Subcategory

class Service(models.Model):
    sname = models.CharField(max_length=100)
    sprice = models.IntegerField()
    sdescription = models.TextField()
    simage = models.ImageField(upload_to='photos')
    scatname = models.ForeignKey(Category, on_delete=models.CASCADE)
    ssubcatname = models.ForeignKey(Subcategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.sname
    def service_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.simage.url))

    service_photo.allow_tags = True

    #View Methods

    @staticmethod
    def get_service_by_catid(cat_id):
        return Service.objects.filter(scatname=cat_id)
    @staticmethod
    def get_service_by_subcatid(subcat_id):
        return Service.objects.filter(ssubcatname=subcat_id)

    @staticmethod
    def get_service_by_id(s_id):
        try:
            return Service.objects.get(id=s_id)
        except:
            return False
    @staticmethod
    def get_service_by_name(s_name):
        try:
            return Service.objects.get(sname=s_name)
        except:
            return False

