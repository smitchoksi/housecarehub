from django.shortcuts import render, redirect,HttpResponse
from HCH.models.user_model import User
from HCH.models.service_model import Service
from HCH.models.manager_model import Manager
from HCH.models.service_man_model import Serviceman
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from urllib.parse import urlencode


def profilefun(request):
    uemail = request.session.get("user_email")
    if uemail:
        userobj = User.get_customer_by_id(uemail)
        if userobj.active:
            services = Service.objects.all()
            context = {
                'services':services,
                'user':userobj
            }
            return render(request, "User Templates/userprofile.html", context)
        else:
            return HttpResponse('<h1>You Are Terminate For This Site</h1>')
    else:
        return render(request,"Error Templates/LoginRequiredError.html")


def updateprofilepic(request):
    uemail = request.session.get("user_email")
    if uemail:
        profilepic = request.FILES["uprofilepic"]
        # print("profile:",profilepic)
        email = request.session.get("user_email")
        userobject = User.objects.get(u_email=email)
        userobject.u_profilepic = profilepic
        userobject.save()
        userobj = User.get_customer_by_id(uemail)
        services = Service.objects.all()
        messages.success(request, "Profile Photo Updated Successfully...")
        return redirect('/profile')
        # context = {
        #     'user': userobj,
        #     'success': "Profile Photo Updated Successfully...",
        #     'services':services
        # }
        # return render(request, "User Templates/userprofile.html", context)
    else:
        return render(request,"Error Templates/LoginRequiredError.html")


def changepasswordfun(request):
    uemail = request.session.get("user_email")
    if uemail:
        oldpass = request.POST.get("oldpassword")
        newpass = request.POST.get("newpassword")
        re_enternewpass = request.POST.get("reenternewpassword")

        uemail = request.session.get("user_email")
        userobj = User.get_customer_by_id(uemail)

        flag = check_password(oldpass, userobj.u_password)

        errormessage = None
        if flag:
            if oldpass==newpass:
                errormessage = "Your old password and new password both is same"
            if newpass != re_enternewpass:
                errormessage = "Re-enter password is not match"

            if len(newpass) >= 8:
                if len(newpass) >= 13:
                    errormessage = "Password should be between 8 - 12 character"
                else:
                    temp = User.passwordvalidation(newpass)
                    if temp == False:
                        errormessage = "Your password is weak 1. Must be use atleast two Special Character like @,#,$,%,& ect, 2. Must be use atleast one Uppercase and three Lowercase 3. Must be use atleast two digits"

            if len(newpass) < 8:
                errormessage = "Password must be minimum 8 Character"
        else:
            errormessage = "Entered Old Password is Wrong"

        if errormessage==None:
            hashpassword = make_password(re_enternewpass)
            userobject = User.objects.filter(u_email=uemail)
            userobject.update(u_password=hashpassword)
            userobj = User.get_customer_by_id(uemail)
            messages.success(request, "Password Changed Successfully...")
            return redirect('/profile')
            # context = {
            #     'user': userobj,
            #     'success': "Password Changed Successfully..."
            # }
            # return render(request, "User Templates/userprofile.html", context)
        else:
            messages.error(request, errormessage)
            return redirect('/profile')
            # userobj = User.get_customer_by_id(uemail)
            # services = Service.objects.all()
            # context = {
            #     'oldpassword':oldpass,
            #     'newpassword':newpass,
            #     'reenternewpassword':re_enternewpass,
            # }
            # messages.error(request, errormessage)
            # query_string = urlencode(context)
            # redirected_url = f"/profile?{query_string}"
            # return redirect(redirected_url)
    else:
        return render(request,"Error Templates/LoginRequiredError.html")


def updateuserprofiledata(request):
    uemail = request.session.get("user_email")
    if uemail:
        f_name = request.POST.get("f_name")
        l_name = request.POST.get("l_name")
        email = request.POST.get("email")
        contactno = request.POST.get("contactno")
        gender = request.POST.get("gender")
        address = request.POST.get("address")
        area = request.POST.get("area")
        age = request.POST.get("age")

        uemail = request.session.get("user_email")
        userobj = User.get_customer_by_id(uemail)
        # print("user object:",userobj,)
        # print("user phoneno:",userobj.u_phoneno, type(userobj.u_phoneno))
        # print("contactno:", contactno, type(contactno))
        errormessage = None
        if int(age) < 12:
            errormessage = "Less than 12 age is not allowed"

        if len(f_name)<3:
            errormessage = "Your first name is not valid"
        if len(l_name)<=3:
            errormessage = "Your last name is not valid"

        if userobj.u_phoneno != int(contactno):
            if User.objects.filter(u_phoneno=contactno):
                errormessage = "Your Contact number is already exists please enter another number"
                # return render(request, "signup.html",{'error':errormessage},value)

        if userobj.u_email != email:
            if User.objects.filter(u_email=email):
                errormessage = "Your email is already exists please enter another email"
                # return render(request, "signup.html",{'error':errormessage},value)

        genderlst = ['Male','male','Female','female','Other','other']
        if gender not in genderlst:
            errormessage = "Please Enter valid Gender like: Male,Female,Other"

        if errormessage == None:
            userobject = User.objects.get(u_email=uemail)
            userobject.u_email=email
            userobject.u_fname=f_name
            userobject.u_lname=l_name
            userobject.u_phoneno=int(contactno)
            userobject.u_address=address
            userobject.u_area=area
            userobject.u_gender=gender
            userobject.u_age=age
            userobject.save()
            request.session["user_email"]=email
            messages.success(request, "Profile Updated Successfully...")
            return redirect('/profile')
            # userobj = User.get_customer_by_id(uemail)
            # services = Service.objects.all()
            # context = {
            #     'user': userobj,
            #     'success': "Profile Updated Successfully...",
            #     'services':services
            # }
            # return render(request, "User Templates/userprofile.html", context)
        else:
            messages.error(request, errormessage)
            return redirect('/profile')
            # userobj = User.get_customer_by_id(uemail)
            # services = Service.objects.all()
            # context = {
            #     'dataerror':errormessage,
            #     'user':userobj,
            #     'services':services
            # }
            # return render(request, "User Templates/userprofile.html", context)
    else:
        return render(request,"Error Templates/LoginRequiredError.html")


def manager_profilefun(request):
    email = request.session.get("manager_email")
    managerobj = Manager.get_manager_by_emailid(email)

    if managerobj:
        name = managerobj.m_name
        email = managerobj.m_email
        contactno = managerobj.m_phoneno
        gender = managerobj.m_gender
        address = managerobj.m_address
        profilepic = managerobj.m_profile_pic
        age = managerobj.m_age
        servicemans = Serviceman.objects.all()
        context = {
            'name':name,
            'email':email,
            'contactno':contactno,
            'gender':gender,
            'address':address,
            'profilepic':profilepic,
            'age':age,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/ManagerProfile.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def serviceman_profile_fun(request):
    email = request.session.get("serviceman_email")
    serviceman_obj = Serviceman.get_serviceman_by_emailid(email)
    if serviceman_obj:
        name = serviceman_obj.sm_name
        email = serviceman_obj.sm_email
        contactno = serviceman_obj.sm_phoneno
        age = serviceman_obj.sm_age
        address = serviceman_obj.sm_address
        gender = serviceman_obj.sm_gender
        category = serviceman_obj.sm_Knowledge_of_category
        work = serviceman_obj.sm_knowledge_of_subcategory
        profilepic = serviceman_obj.sm_profile_pic

        context = {
            'name':name,
            'email':email,
            'contactno':contactno,
            'age':age,
            'address':address,
            'gender':gender,
            'category':category,
            'work':work,
            'profilepic':profilepic
        }
        return render(request, "Serviceman Templates/ServicemanProfile.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def view_serviceman_profile_by_manager(request,serviceman_id):
    servicemanobj = Serviceman.objects.get(id=serviceman_id)
    context={
        'serviceman':servicemanobj
    }
    return render(request, "Manager Templates/ViewServicemanProfile.html", context)