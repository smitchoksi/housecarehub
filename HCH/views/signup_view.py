from django.shortcuts import render, redirect
from HCH.models.user_model import User
from HCH.models.category_model import Category
from HCH.models.service_model import Service
from django.contrib.auth.hashers import make_password
from HCH.models.manager_model import Manager
from HCH.models.service_man_model import Serviceman
from django.contrib import messages
def signuppage(request):
    services = Service.objects.all()
    context={
        'services':services
    }
    return render(request, "User Templates/signup.html",context)

def register_fun(request):
    fname = request.POST.get("ufirstname")
    lname = request.POST.get("ulastname")
    email = request.POST.get("uemail")
    contactno = request.POST.get("umobileno")
    gender = request.POST.get("ugender")
    age = request.POST.get("uage")
    create_password = request.POST.get("ucreatepassword")
    reenter_password = request.POST.get("ureenterpassword")

    value = {
        'fname':fname,
        'lname': lname,
        'email': email,
        'contactno': contactno,
        'gender': gender,
        'create_password':create_password,
        'reenter_password':reenter_password,
        'uage':age
    }
    errormessage = None


    if create_password != reenter_password:
        errormessage = "Re-enter password is not match"

    if len(create_password) >= 8:
        if len(create_password) >= 13:
            errormessage = "Password should ne between 8 - 12 character"
        else:
            temp = User.passwordvalidation(create_password)
            if temp == False:
                errormessage = "Your password is weak \n1. Must be use atleast two Special Character like @,#,$,%,& ect, \n2. Must be use atleast one Uppercase and three Lowercase \n3. Must be use atleast two digits"

    if len(create_password) < 8:
        errormessage = "Password must be minimum 8 Character"
        # return render(request, "signup.html", {'error': errormessage},value)

    if int(age) < 12:
        errormessage = "Your are not eligible for singup because your age is less than 12"

    if len(fname)<3:
        errormessage = "Your first name is not valid"
    if len(lname)<=3:
        errormessage = "Your last name is not valid"

    if User.objects.filter(u_phoneno=contactno):
        errormessage = "Your Contact number is already exists please enter another number"
        # return render(request, "signup.html",{'error':errormessage},value)

    if User.objects.filter(u_email=email):
        errormessage = "Your email is already exists please enter another email"
        # return render(request, "signup.html",{'error':errormessage},value)
    elif Manager.objects.filter(m_email=email):
            errormessage = "Your email is already exists please enter another email"
    elif Serviceman.objects.filter(sm_email=email):
        errormessage = "Your email is already exists please enter another email"

    if errormessage is None:
        hashpassword = make_password(reenter_password)
        userdata = User(u_email=email,
                        u_password=hashpassword,
                        u_fname=fname,
                        u_lname=lname,
                        u_phoneno=contactno,
                        u_gender=gender,
                        u_age = age,)

        userdata.save()
        request.session["user_id"] = userdata.id
        request.session["user_email"] = email
        messages.success(request, "Your Account Created Successfully...")
        return redirect('/')
        # Render index.html page
        # category_objects = Category.get_all_category()
        # services = Service.objects.all()
        # context = {
        #     'category': category_objects,
        #     'services': services,
        #     'success': "Your Account Created Successfully..."
        # }
        # return render(request, "User Templates/index.html", context)
    else:
        services = Service.objects.all()
        context = {
            # 'error': errormessage,
            'udata': value,
            'services': services
        }
        messages.error(request, errormessage)
        return render(request, "User Templates/signup.html", context)
