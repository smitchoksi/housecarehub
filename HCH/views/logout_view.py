from django.shortcuts import render, redirect
from HCH.models.category_model import Category
from HCH.models.service_model import Service
from HCH.models.service_man_model import Serviceman
from urllib.parse import urlencode
from datetime import datetime
from django.contrib import messages

def user_logout_fun(request):
    print("Function is called")
    uemail = request.session.get("user_email")
    if uemail:
        del request.session["user_id"]
        del request.session["user_email"]
        messages.success(request, "Logout Done Successfully...")
        # query_string = urlencode(context)
        # redirected_url = f'/?{query_string}'
        return redirect("/")
        # return render(request, "User Templates/index.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def manager_logout_fun(request):
    memail = request.session.get("manager_email")
    if memail:
        del request.session["manager_id"]
        del request.session["manager_email"]
        messages.success(request, "Logout Done Successfully...")
        return redirect("/")
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def serviceman_logout_fun(request):
    semail = request.session.get("serviceman_email")
    if semail:
        servicemanobj = Serviceman.objects.get(id=int(request.session["serviceman_id"]))
        todaydate_time = datetime.now()
        servicemanobj.last_logout_time = todaydate_time
        servicemanobj.save()
        del request.session["serviceman_id"]
        del request.session["serviceman_email"]
        messages.success(request, "Logout Done Successfully...")
        return redirect("/")
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

