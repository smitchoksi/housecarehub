from django.shortcuts import render, redirect
from HCH.models.service_man_model import Serviceman

def fetch_servicemanlist(request):
    manager = request.session.get("manager_email")
    if manager:
        serviceman_obj = Serviceman.get_all_serviceman()
        context= {
            'listofserviceman':serviceman_obj,
            'servicemans': serviceman_obj
        }
        return render(request, "Manager Templates/Servicemanlist.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def fetch_servicemanlist_by_category(request,cat_id):
    manager = request.session.get("manager_email")
    if manager:
        serviceman_obj = Serviceman.get_serviceman_by_category(cat_id)
        servicemans = Serviceman.objects.all()
        context = {
            'servicemans':servicemans,
            'listofserviceman': serviceman_obj
        }
        return render(request, "Manager Templates/Servicemanlist.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")