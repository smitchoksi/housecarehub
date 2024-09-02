from django.shortcuts import render, redirect
from HCH.models.subcategory_model import Subcategory
from HCH.models.service_model import Service

def subcategorypage(request, cat_id):
    #function call from Subcategory model
    subcategory = Subcategory.get_subcategory_of_category(cat_id)
    services = Service.objects.all()
    #print(subcategory)
    context={
        'subcategory':subcategory,
        'services': services
    }
    return render(request, "User Templates/subcategorypage.html",context)