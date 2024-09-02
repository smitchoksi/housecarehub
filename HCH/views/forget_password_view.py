from django.shortcuts import render, redirect, HttpResponse
from HCH.models.user_model import User
from HCH.models.category_model import Category
from HCH.models.service_model import Service
from .otp_view import send_otp_for_forgetpassword
from datetime import datetime,date,timedelta
from django.contrib.auth.hashers import make_password
from urllib.parse import urlencode
from django.contrib import messages

def forgetpassword_page(request):   # /forgetpassword_page
    services = Service.objects.all()
    if request.GET.get('url'):
        context = {
            'url': request.GET.get('url'),
            'services': services,
            'otp': request.GET.get('otp'),
            'success': request.GET.get('success'),
            'error': request.GET.get('error'),
            'email': request.GET.get('email'),
            'regenerate_opt': request.GET.get('regenerate_opt'),
            'otperror': request.GET.get('otperror'),
        }
        return render(request, "User Templates/ForgetPassword.html", context)
    else:
        context = {
            'url':"forgetpassword",
            'services':services
        }
        return render(request, "User Templates/ForgetPassword.html",context)

def forgetpassword_page2(request):  #/forgetpassword_page2
    services = Service.objects.all()
    context = {
        'error': request.GET.get('error'),
        'success': request.GET.get('success'),
        'url': request.GET.get('url'),
        'email': request.GET.get('email'),
        'createpassword': request.GET.get('createpassword'),
        'reenterpassword': request.GET.get('reenterpassword'),
        'services': services
    }
    if request.GET.get('createpassword')==None:
        for i in context:
            if i == 'createpassword':
                context[i]=''

    if request.GET.get('reenterpassword')==None:
        for i in context:
            if i == 'reenterpassword':
                context[i]=''
    return render(request,"User Templates/ForgetPassword2.html",context)

def forgetpassword_fun(request):    #/forgetpassword  Form Submit Action Url
    uemail = request.POST.get("email")
    try:
        userobj = User.objects.get(u_email=uemail)
    except:
        # errormsg = "Your Email Id is Not Exist"
        messages.error(request, "Your Email Id is Not Exist")
        services = Service.objects.all()
        context = {
            'url': "forgetpassword",
            # 'error': errormsg,
            'email':uemail,
            'services':services
        }
        query_string = urlencode(context)
        redirected_url = f'/forgetpassword_page?{query_string}'
        return redirect(redirected_url)
        # return render(request, "User Templates/ForgetPassword.html", context)

    if userobj:
        send_otp_for_forgetpassword(request,uemail)
        context = {
            'url':"forgetpass_otpverification",
            'otp':True,
            # 'success': "OTP Sended To Your Email...",
            'email':uemail,
            # 'services':services
        }
        messages.success(request, "OTP Sended To Your Email...")
        query_string = urlencode(context)
        redirected_url = f'/forgetpassword_page?{query_string}'
        return redirect(redirected_url)

    return render(request, "User Templates/ForgetPassword.html")

def forgetpass_otpverification_fun(request): #/forgetpass_otpverification  Form Submit Action Url
    uemail = request.POST.get("email")
    otp = request.POST.get("otp")
    sendedopt = request.session.get("OTP")
    time_session = request.session.get("Time")
    time_obj = datetime.strptime(time_session, "%Y-%m-%d %H:%M:%S.%f")
    send_again = time_obj + timedelta(minutes=1)
    expire_time = time_obj + timedelta(minutes=5)
    flag = 0
    error_message = None
    if datetime.now() > expire_time:
        flag = 1
        error_message = "OTP is Expire"

    if otp == sendedopt:
        pass
    else:
        flag = 1
        error_message = "Entered OTP is Wrong"


    if flag and error_message != None:
        if datetime.now() > send_again:
            services = Service.objects.all()
            context = {
                'url': "forgetpass_otpverification",
                'regenerate_opt': True,
                'otp': True,
                'email': uemail,
                # 'error': error_message,
                'otperror': True,
                'services':services
            }
            messages.error(request, error_message)
            return render(request, "User Templates/ForgetPassword.html", context)
        else:
            services = Service.objects.all()
            context = {
                'url': "forgetpass_otpverification",
                'regenerate_opt':False,
                'otp': True,
                'email': uemail,
                # 'error': error_message,
                'otperror':True,
                'services':services
            }
            messages.error(request, error_message)
            return render(request, "User Templates/ForgetPassword.html", context)
    elif flag == 0 and error_message == None:
        context = {
            # 'success': "OTP Verification Done Successfully...",
            'url': 'check_forgetpass_details',
            'email':uemail,
        }
        messages.success(request, "OTP Verification Done Successfully...")
        query_string = urlencode(context)
        redirected_url = f'/forgetpassword_page2?{query_string}'
        return redirect(redirected_url)

def check_forgetpass_details(request): #/check_forgetpass_details  Form Submit Action Url
    uemail = request.POST.get("email")
    print(uemail)
    createpassword = request.POST.get("createpassword")
    reenterpassword = request.POST.get("reenterpassword")
    errormsg = None
    if createpassword != reenterpassword:
        errormsg = "Re-enter password is not match"

    if len(createpassword) >= 8:
        if len(createpassword) >= 13:
            errormsg = "Password should ne between 8 - 12 character"
        else:
            print(createpassword, "is checking")
            temp = User.passwordvalidation(createpassword)
            if temp == False:
                errormsg = "Your password is weak \n1. Must be use atleast two Special Character like @,#,$,%,& ect, \n2. Must be use atleast one Uppercase and three Lowercase \n3. Must be use atleast two digits"

    if len(createpassword) < 8:
        errormsg = "Password must be minimum 8 Character"

    if errormsg == None:
        hashpassword = make_password(reenterpassword)
        userobj = User.objects.get(u_email=uemail)
        userobj.u_password=hashpassword
        userobj.save()
        if request.session["user_id"]:
            del request.session["user_id"]
            del request.session["user_email"]
        # context = {
        #     'success': "Your Password is Forget Successfully..."
        # }
        messages.success(request, "Your Password is Forget Successfully...")
        # query_string = urlencode(context)
        # redirected_url = f'/loginpage?{query_string}'
        return redirect('/loginpage')
        # return render(request, "User Templates/Login.html", context)
    else:
        services = Service.objects.all()
        context = {
            'email': uemail,
            'url':"check_forgetpass_details",
            'createpassword':createpassword,
            'reenterpassword':reenterpassword,
            'error': errormsg,
            'services':services
        }
        messages.error(request, errormsg)
        query_string = urlencode(context)
        redirected_url = f'/forgetpassword_page2?{query_string}'
        return redirect(redirected_url)
        # return render(request, "User Templates/ForgetPassword2.html", context)

def regenerate_otp(request,email):
    try:
        userobj = User.objects.get(u_email=email)
    except:
        # errormsg = "Your Email Id is Not Exist"
        messages.error(request, "Your Email Id is Not Exist""Your Email Id is Not Exist")
        services = Service.objects.all()
        context = {
            'url': "forgetpassword",
            # 'error': errormsg,
            'email': email,
            'services':services
        }
        return render(request, "User Templates/ForgetPassword.html", context)

    if userobj:
        send_otp_for_forgetpassword(request, email)
        services = Service.objects.all()
        context = {
            'url': "forgetpass_otpverification",
            'otp': True,
            # 'success': "OTP Sended To Your Email...",
            'email': email,
            'otperror':True,
            'services':services
        }
        messages.success(request, "OTP Sended To Your Email...")
        return render(request, "User Templates/ForgetPassword.html", context)

    return render(request, "User Templates/ForgetPassword.html")
