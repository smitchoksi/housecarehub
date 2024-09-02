from django.db import models
from django.utils.safestring import mark_safe

m_gender_choice = [
    ("Male","Male"),
    ("Female","Female"),
    ("Other","Other")
]
class Manager(models.Model):
    m_email = models.EmailField()
    m_password = models.CharField(max_length=256)
    m_name = models.CharField(max_length=100)
    m_phoneno = models.BigIntegerField()
    sm_work_experience = models.CharField(max_length=20)
    m_age = models.IntegerField()
    m_address = models.TextField()
    m_gender = models.CharField(choices=m_gender_choice, max_length=10)
    m_profile_pic = models.ImageField(upload_to='manager')
    m_adharno = models.BigIntegerField()
    m_adharphoto = models.ImageField(upload_to='manager')
    m_salary = models.IntegerField()
    instaff = models.BooleanField(default=True)

    def manager_profile_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.m_profile_pic.url))

    manager_profile_photo.allow_tags = True

    def manager_adhar_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.m_adharphoto.url))

    manager_adhar_photo.allow_tags = True

    @staticmethod
    def get_manager_by_emailid(email):
        try:
            return Manager.objects.get(m_email=email)
        except:
            return False