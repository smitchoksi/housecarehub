from django.db import models
from django.utils.safestring import mark_safe


class User(models.Model):
    u_email = models.EmailField(unique=True)
    u_password = models.CharField(max_length=256)
    u_fname = models.CharField(max_length=50)
    u_lname = models.CharField(max_length=50)
    u_phoneno = models.BigIntegerField()
    u_address = models.TextField(null=True)
    u_area = models.CharField(max_length=30, null=True)
    u_gender = models.CharField( max_length=10, null=True)
    u_age = models.IntegerField()
    u_profilepic = models.ImageField(default="user/Default_User_Photo.jpg",upload_to='user', null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.u_email
    def user_profile_photo(self):
        return mark_safe('<img src="{}" width="100"/>'.format(self.u_profilepic.url))

    user_profile_photo.allow_tags = True

    #View Function
    def passwordvalidation(password):
        # print("function called")
        specialchacter = ["{","}","(",")","[","]","#",":",";","^",",",".","?","!","|","&","_","`","~","@","$","%","/","+","=","-","*",'"',"'"]
        if len(password)>=8:
            specialcount=0
            uppercasecaount=0
            lowercasecaount=0
            digitcount=0
            for i in password:
                if i in specialchacter:
                    specialcount=specialcount+1

                if i>="A" and i<="Z":
                    uppercasecaount=uppercasecaount+1

                if i>="a" and i<="z":
                    lowercasecaount=lowercasecaount+1

                if i>="0" and i<="9":
                    digitcount=digitcount+1

            if specialcount>=2 and uppercasecaount>=1 and lowercasecaount>=3 and digitcount>=2:
                # print("specialcount", specialcount)
                # print("uppercasecaount", uppercasecaount)
                # print("lowercasecaount", lowercasecaount)
                # print("digitcount", digitcount)
                return True
            else:
                # print("specialcount",specialcount)
                # print("uppercasecaount",uppercasecaount)
                # print("lowercasecaount",lowercasecaount)
                # print("digitcount",digitcount)

                return False
    @staticmethod
    def get_customer_by_id(uemail):
        try:
            return User.objects.get(u_email=uemail)
        except:
            return False

    @staticmethod
    def get_uerobj_by_email(uemail):
        try:
            return User.objects.filter(u_email=uemail)
        except:
            return False
