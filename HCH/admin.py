from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import User as Predefine_User
admin.site.unregister(Group)
admin.site.unregister(Predefine_User)

from .models.category_model import Category
from .models.subcategory_model import Subcategory
from .models.service_model import Service
from .models.user_model import User
from .models.sparepart_title_model import Spareparttitle
from .models.sparepart_model import Sparepart
from .models.manager_model import Manager
from .models.service_man_model import Serviceman
from .models.booking_model import Booking
from .models.payment_details_model import Paymentdetails
from .models.sparepart_payment_model import Sparepart_payment
from .models.feedback_rating_model import Feedback_rating
from .models.complaint_model import Complaint
from .models.task_model import Task
from .models.updated_sparepart_model import Updated_Sparepart

# Register your models here.
admin.site.site_header="HCH Administration"
class Showcategory(admin.ModelAdmin):
    list_display = ["id","catname","category_photo"]
    search_fields = ['catname']
    # list_filter = ['catname']
admin.site.register(Category,Showcategory)

class Showsubcategory(admin.ModelAdmin):
    list_display = ["id","subcatname","catname","subcategory_photo"]
    search_fields = ['subcatname']
    list_filter = ['catname']

admin.site.register(Subcategory,Showsubcategory)

class Showservice(admin.ModelAdmin):
    list_display = ["id","sname","sprice","sdescription","scatname","ssubcatname","service_photo"]
    search_fields = ['sname']
    list_filter = ['scatname','ssubcatname']
admin.site.register(Service, Showservice)

class Showuser(admin.ModelAdmin):
    list_display = ["id","u_email", "u_password", "u_fname", "u_lname", "u_phoneno", "u_address", "u_area", "u_gender", "u_age", "user_profile_photo"]
    search_fields = ['u_email']
    list_filter = ['u_gender']
admin.site.register(User, Showuser)

class Showspareparttitle(admin.ModelAdmin):
    list_display = ["id","sp_title", "sp_category", "sp_subcategory"]
    search_fields = ['sp_title']
    list_filter = ['sp_category','sp_subcategory']

admin.site.register(Spareparttitle, Showspareparttitle)

class Showsparepart(admin.ModelAdmin):
    list_display = ["id","sparepart_title", "sparepart_name", "sparepart_price", "sparepart_quantity"]
    search_fields = ['sparepart_name']

admin.site.register(Sparepart, Showsparepart)

class Showmanager(admin.ModelAdmin):
    list_display = ["id","m_email", "m_password", "m_name", "m_phoneno", "m_age","sm_work_experience", "m_address", "m_gender", "m_profile_pic", "m_adharno", "m_adharphoto", "m_salary"]
    search_fields = ['id','m_email','m_name']

admin.site.register(Manager, Showmanager)

class Showserviceman(admin.ModelAdmin):
    list_display = ["id","sm_email","sm_password","sm_name","sm_phoneno","sm_age","sm_Knowledge_of_category","sm_knowledge_of_subcategory","sm_work_experience","sm_address","sm_gender","sm_profile_pic","sm_adharno","sm_adharphoto","sm_status","sm_salary","sm_d_o_j","sm_d_o_l","last_login_time","last_logout_time","instaff"]
    search_fields = ['id','sm_email','sm_name']
    list_filter = ['sm_Knowledge_of_category','sm_status']

admin.site.register(Serviceman, Showserviceman)

class Showbooking(admin.ModelAdmin):
    list_display = ["id","name", "contactno","address","area","city","state","country", "booking_date_time", "booking_provide_date", "booking_provide_time","booking_status","user_id","service_id"]
    search_fields = ['id','name']
admin.site.register(Booking, Showbooking)

class Showtask(admin.ModelAdmin):
    list_display = ["id","booking_id","status","serviceman_id","assign_time","pick_time","start_time","complete_time","need_sparepart","close_task"]
    search_fields = ['booking_id']
    list_filter = ['status']
admin.site.register(Task,Showtask)

class Showpaymentdetails(admin.ModelAdmin):
    list_display = ["id","booking_id","service_id","user_id","upi_id","amount","tax","totalamount"]
    search_fields = ['booking_id']
admin.site.register(Paymentdetails, Showpaymentdetails)

class Showsparepart_payment(admin.ModelAdmin):
    list_display = ["id","sparepart_tax","sparepart_total_amount","booking_id","task_id", "upi_id"]
    filter_horizontal = ('updated_spareparts',)
    search_fields = ['booking_id']

admin.site.register(Sparepart_payment, Showsparepart_payment)

class Showfeedback_rating(admin.ModelAdmin):
    list_display = ["id","rating","feedback_title","feedback_description","feedback_datetime","user_id","service_id","booking_id"]
    search_fields = ['service_id']
    list_filter = ['rating']

admin.site.register(Feedback_rating, Showfeedback_rating)

class Showcomplaint(admin.ModelAdmin):
    list_display = ["id","complaint_date","complaint_topic","complaint_pic","complaint_description","complaint_status","user_id","booking_id", "service_id"]
    search_fields = ['booking_id']
    list_filter = ['complaint_status']

admin.site.register(Complaint, Showcomplaint)

class Showupdatedsparepart(admin.ModelAdmin):
    list_display = ["id","task_id","sparepart_id","quantity","square_feet"]
    # filter_horizontal = ('sparepart_ids',)
    search_fields = ['task_id']
admin.site.register(Updated_Sparepart, Showupdatedsparepart)



