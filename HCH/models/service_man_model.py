from django.db import models
from django.utils.safestring import mark_safe
from .category_model import Category
from .subcategory_model import Subcategory
sm_gender_choice = [
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other")
]

class Serviceman(models.Model):
    sm_email = models.EmailField()
    sm_password = models.CharField(max_length=256)
    sm_name = models.CharField(max_length=100)
    sm_phoneno = models.BigIntegerField()
    sm_age = models.IntegerField()
    sm_address = models.TextField()
    sm_gender = models.CharField(choices=sm_gender_choice, max_length=10)
    sm_Knowledge_of_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sm_knowledge_of_subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    sm_work_experience = models.CharField(max_length=20)
    sm_profile_pic = models.ImageField(upload_to='serviceman')
    sm_adharno = models.BigIntegerField()
    sm_adharphoto = models.ImageField(upload_to='serviceman')
    sm_status = models.CharField(max_length=50)         # Allocated, Available, On Holiday
    sm_salary = models.IntegerField()
    sm_d_o_j = models.DateField()
    sm_d_o_l = models.DateField(null=True,blank=True)
    last_login_time = models.DateTimeField(null=True, blank=True)
    last_logout_time = models.DateTimeField(null=True, blank=True)
    instaff = models.BooleanField(default=True)


    def __str__(self):
        return self.sm_name
    def serviceman_profile_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.sm_profile_pic.url))

    serviceman_profile_photo.allow_tags = True

    def serviceman_adhar_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.sm_adharphoto.url))

    serviceman_adhar_photo.allow_tags = True

    @staticmethod
    def get_serviceman_by_emailid(email):
        try:
            return Serviceman.objects.get(sm_email=email)
        except:
            return False

    @staticmethod
    def get_all_serviceman():
        try:
            return Serviceman.objects.all()
        except:
            return False

    @staticmethod
    def get_serviceman_by_category(cat_id):
        try:
            return Serviceman.objects.filter(sm_Knowledge_of_category=cat_id)
        except:
            return False