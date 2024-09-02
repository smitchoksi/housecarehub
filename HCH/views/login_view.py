from django.shortcuts import render, redirect
from HCH.models.user_model import User
from HCH.models.manager_model import Manager
from HCH.models.category_model import Category
from HCH.models.service_model import Service
from HCH.models.service_man_model import Serviceman
from django.contrib.auth.hashers import check_password
from datetime import datetime
from urllib.parse import urlencode
from django.contrib import messages

def loginpage(request):
    services = Service.objects.all()
    if request.GET.get('uemail'):
        context = {
            'success':request.GET.get('success'),
            'uemail':request.GET.get('uemail'),
            'upassword':request.GET.get('upassword'),
            'services':services
        }
    else:
        context = {
            'services': services
        }
    return render(request, "User Templates/login.html",context)

def checklogin_details(request):
    uemail = request.POST.get("email")
    upassword = request.POST.get("password")
    # print(uemail, upassword)

    errormessage = None

    customerobj = User.get_customer_by_id(uemail)  # function called
    #print(customerobj,"user id:",customerobj.id, "user email:", customerobj.u_email)

    if customerobj:
        if customerobj.active:
            flag = check_password(upassword, customerobj.u_password)
            if flag:
                request.session["user_id"] = customerobj.id
                request.session["user_email"] = customerobj.u_email
                messages.success(request, "Login Done Successfully...")
                return redirect('/')
            else:
                errormessage = "Your Password is wrong"
        else:
            errormessage = "Your Are Terminate for This Site"
    else:
        managerobj = Manager.get_manager_by_emailid(uemail)
        if managerobj:
            if managerobj.instaff == True:
                #flag = check_password(upassword, managerobj.m_password)
                if upassword == managerobj.m_password:
                    request.session["manager_id"] = managerobj.id
                    request.session["manager_email"] = managerobj.m_email
                    messages.success(request, "Login Done Successfully...")
                    return redirect('/manager_dashboard')
                    # return render(request, "Manager Templates/ManagerDashboard.html")
                else:
                    errormessage = "Entered Password Is Wrong"
            else:
                errormessage = "Your Are Terminate For This Site"
        else:
            servicemanobj = Serviceman.get_serviceman_by_emailid(uemail)
            if servicemanobj:
                if servicemanobj.instaff == True:
                    #flag = check_password(upassword, servicemanobj.sm_password)
                    if upassword == servicemanobj.sm_password:
                        request.session["serviceman_id"] = servicemanobj.id
                        request.session["serviceman_email"] = servicemanobj.sm_email
                        todaydate_time = datetime.now()
                        servicemanobj.last_login_time = todaydate_time
                        servicemanobj.save()
                        messages.success(request, "Login Done Successfully...")
                        return redirect('/serviceman_dashboard')
                        # return render(request, "Serviceman Templates/ServicemanDashboard.html")
                    else:
                        errormessage = "Entered Password Is Wrong"
                else:
                    errormessage = "Your Are Terminate For This Site"

            else:
                errormessage = "Your email id does not exist"

    services = Service.objects.all()
    context = {
        # 'error': errormessage,
        'uemail': uemail,
        'upassword': upassword,
        'services':services
    }
    messages.error(request, errormessage)
    query_string = urlencode(context)
    redirected_url = f"/loginpage?{query_string}"
    return redirect(redirected_url)
    # return render(request, "User Templates/login.html", context)