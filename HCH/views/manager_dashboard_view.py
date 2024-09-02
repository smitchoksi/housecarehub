from django.shortcuts import render, redirect, HttpResponse
from HCH.models.category_model import Category
from HCH.models.service_man_model import Serviceman

def manager_dashboard_page(request):
    manager = request.session.get("manager_email")
    if manager:
        servicemans = Serviceman.objects.all()
        context = {
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/ManagerDashboard.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def show_category_list_for_serviceman(request):
    manager = request.session.get("manager_email")
    if manager:
        category_objects = Category.get_all_category()
        servicemans = Serviceman.objects.all()
        context = {
            'category': category_objects,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/ListofCategory.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

