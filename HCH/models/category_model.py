from django.db import models
from django.utils.safestring import mark_safe

class Category(models.Model):
    catname = models.CharField(max_length=256, null=False)
    catimage = models.ImageField(upload_to='category', null=False)

    def __str__(self):
        return self.catname
    def category_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.catimage.url))

    category_photo.allow_tags = True

    # Views methods...
    @staticmethod
    def get_all_category():
        return Category.objects.all()