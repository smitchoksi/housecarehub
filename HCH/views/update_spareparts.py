from django.shortcuts import render, redirect, HttpResponse
from HCH.models.task_model import Task
from HCH.models.sparepart_title_model import Spareparttitle
from HCH.models.sparepart_model import Sparepart
from HCH.models.booking_model import Booking
from HCH.models.service_model import Service
from HCH.models.updated_sparepart_model import Updated_Sparepart
from HCH.models.sparepart_payment_model import Sparepart_payment
from urllib.parse import urlencode
from django.contrib import messages

def update_spareparts_page(request,task_id):
    taskobj = Task.objects.get(id=task_id)
    cat_id = taskobj.booking_id.service_id.scatname
    # print("Category:",cat_id)
    subcat_id = taskobj.booking_id.service_id.ssubcatname
    # print("subcategory:",subcat_id)
    sp_titles = Spareparttitle.objects.filter(sp_category=cat_id,sp_subcategory=subcat_id)

    if request.GET.get('url'):
        title_id=request.GET.get('title_id')
        sptitle_obj = Spareparttitle.objects.get(id=title_id,
                                                 sp_subcategory=taskobj.booking_id.service_id.ssubcatname)

        spobj = Sparepart.objects.filter(sparepart_title=sptitle_obj.id)
        context = {
            'url': request.GET.get('url'),
            'task_id': task_id,
            'titles': sp_titles,
            # 'done': request.GET.get('done'),
            'title': request.GET.get('title'),
            'sparepart': spobj,
            'error': request.GET.get('error'),
            'sptitle_obj':sptitle_obj
        }
        return render(request, "Serviceman Templates/UpdateSpareparts.html", context)

    else:
        context = {
            'url':"fetch_sparepartname_list",
            'task_id':task_id,
            'titles':sp_titles,
        }
        return render(request,"Serviceman Templates/UpdateSpareparts.html",context)

def fetch_sparepartname_list(request):
    title_id = request.POST.get("title_id")
    task_id = request.POST.get("task_id")
    if title_id != "None":
        # sparepart_title = Spareparttitle.objects.get(id=title_id)
        taskobj = Task.objects.get(id=task_id)
        subcat_id = taskobj.booking_id.service_id.ssubcatname
        sptitle_obj = Spareparttitle.objects.get(id=title_id, sp_subcategory=subcat_id)
        spobj = Sparepart.objects.filter(sparepart_title=sptitle_obj.id)  # sparepart obj
        # for i in spobj:
        #     print(i.sparepart_name)
        context = {
            'task_id': task_id,
            'url': 'update_name',
            'title_id': title_id,
            'sparepart': spobj,
            'sptitle_obj': sptitle_obj
        }
        return render(request, "Serviceman Templates/UpdateSpareparts.html", context)
    else:
        taskobj = Task.objects.get(id=task_id)
        sp_titles = Spareparttitle.objects.filter(sp_category=taskobj.booking_id.service_id.scatname, sp_subcategory=taskobj.booking_id.service_id.ssubcatname)

        context = {
            'error': "Please Select Title",
            'task_id': task_id,
            'url': 'fetch_sparepartname_list',
            'titles': sp_titles
        }
        return render(request,"Serviceman Templates/UpdateSpareparts.html",context)


def update_sparepart(request):
    title_name = request.POST.get("title_id")
    task_id = int(request.POST.get("task_id"))
    taskobj = Task.objects.get(id=task_id)
    # print("sp sub category:",taskobj.booking_id.service_id.ssubcatname)
    sptitle_obj = Spareparttitle.objects.get(sp_title=title_name, sp_subcategory=taskobj.booking_id.service_id.ssubcatname)

    sparepart_id = request.POST.get("sparepart")

    if sparepart_id == "None":
        spobj = Sparepart.objects.filter(sparepart_title=sptitle_obj.id)
        context = {
            # 'error': "Please Select Name...",
            'task_id': task_id,
            'url': 'update_name',
            'title_id': sptitle_obj.id,
            'sparepart': spobj,
            'sptitle_obj': sptitle_obj
        }
        messages.error(request, "Please Select Name...")
        query_string = urlencode(context)
        redirected_url = f'/updatespareparts_page/{task_id}?{query_string}'
        return redirect(redirected_url)
    else:
        spobj = Sparepart.objects.get(id=sparepart_id)
        usp = Updated_Sparepart.objects.filter(task_id=taskobj.id)
        for i in usp:
            if spobj.id == i.sparepart_id.id:
                context = {
                    # 'error': "This is Already Updated",
                    'task_id': task_id,
                    'url': 'update_name',
                    'title_id': sptitle_obj.id,
                    'sparepart': spobj,
                    'sptitle_obj': sptitle_obj
                }
                messages.error(request, "This Sparepart is Already Updated")
                query_string = urlencode(context)
                redirected_url = f'/updatespareparts_page/{task_id}?{query_string}'
                return redirect(redirected_url)

    quantity = request.POST.get("quantity")
    sqrfeet = request.POST.get("sqrfeet")
    spobj = Sparepart.objects.get(id=sparepart_id)

    if taskobj.booking_id.service_id.scatname.catname != "Appliance":
        if sqrfeet:
            sqrfeet = int(sqrfeet)
            if sqrfeet <= 1:
                # sparepart_title = Spareparttitle.objects.get(id=sp_titleobj.id)
                spobj = Sparepart.objects.filter(sparepart_title=sptitle_obj.id)
                context = {
                    # 'error': "Please Insert Square Feet...",
                    'task_id': task_id,
                    'url': 'update_name',
                    'title_id': sptitle_obj.id,
                    'sparepart': spobj,
                    'sptitle_obj':sptitle_obj
                }
                messages.error(request, "Please Insert Square Feet...")
                query_string = urlencode(context)
                redirected_url = f'/updatespareparts_page/{task_id}?{query_string}'
                return redirect(redirected_url)
            else:
                updated_sp = Updated_Sparepart(task_id=Task(id=task_id), sparepart_id=Sparepart(id=sparepart_id),
                                               square_feet=int(sqrfeet))
                updated_sp.save()
        else:
            context = {
                # 'done':True,
                # 'error': "Please Insert Square Feet...",
                'task_id': task_id,
                'url': 'update_name',
                'title_id': sptitle_obj.id,
                'sparepart': spobj,
                'sptitle_obj': sptitle_obj
            }
            messages.error(request, "Please Insert Square Feet...")
            query_string = urlencode(context)
            redirected_url = f'/updatespareparts_page/{task_id}?{query_string}'
            return redirect(redirected_url)

    if taskobj.booking_id.service_id.scatname.catname == "Appliance":
        if quantity:
            quantity = int(quantity)
            if spobj.sparepart_quantity != None and quantity >= 1:
                updated_sp = Updated_Sparepart(task_id=Task(id=task_id), sparepart_id=Sparepart(id=sparepart_id), quantity=quantity)
                updated_sp.save()
            else:
                context = {
                    # 'done':True,
                    # 'error': "Please Insert Quantity...",
                    'task_id': task_id,
                    'url': 'update_name',
                    'title_id': sptitle_obj.id,
                    'sparepart': spobj,
                    'sptitle_obj':sptitle_obj
                }
                messages.error(request, "Please Insert Quantity...")
                query_string = urlencode(context)
                redirected_url = f'/updatespareparts_page/{task_id}?{query_string}'
                return redirect(redirected_url)
        else:
            if spobj.sparepart_quantity != None:
                context = {
                    # 'done':True,
                    # 'error': "Please Insert Quantity...",
                    'task_id': task_id,
                    'url': 'update_name',
                    'title_id': sptitle_obj.id,
                    'sparepart': spobj,
                    'sptitle_obj': sptitle_obj
                }
                messages.error(request, "Please Insert Quantity...")
                query_string = urlencode(context)
                redirected_url = f'/updatespareparts_page/{task_id}?{query_string}'
                return redirect(redirected_url)
            elif spobj.sparepart_quantity==None:
                updated_sp = Updated_Sparepart(task_id=Task(id=task_id), sparepart_id=Sparepart(id=sparepart_id))
                updated_sp.save()

    spobj = Sparepart.objects.filter(sparepart_title=sptitle_obj.id)
    context = {
        'task_id':task_id,
        'url': 'update_name',
        'title_id': sptitle_obj.id,
        'sparepart': spobj,
        'sptitle_obj':sptitle_obj
    }
    messages.success(request, "Sparepart Updated Successfully...")
    query_string = urlencode(context)
    redirected_url = f'/updatespareparts_page/{task_id}?{query_string}'
    return redirect(redirected_url)
    # return render(request, "Serviceman Templates/UpdateSpareparts.html", context)


def updated_sparepartname(request,task_id):
    updated_sp = Updated_Sparepart.objects.filter(task_id=task_id)
    updated_sp_copy = Updated_Sparepart.objects.filter(task_id=task_id)

    amount=0
    for i in updated_sp:
        if i.quantity!=None:
            if i.quantity > 1:
                amount = amount + i.sparepart_id.sparepart_price * i.quantity
            else:
                amount = amount + i.sparepart_id.sparepart_price
        else:
            if i.square_feet != None:
                amount = amount + i.sparepart_id.sparepart_price * i.square_feet
            else:
                amount = amount + i.sparepart_id.sparepart_price

    tax = amount * 18 / 100
    tax = round(tax,2)
    total = amount + tax
    total = round(total, 2)
    taskobj = Task.objects.get(id=task_id)
    catname = taskobj.booking_id.service_id.scatname.catname
    context = {
        'catname': catname,
        'task_id':task_id,
        'total':total,
        'tax':tax,
        'updated_spareparts':updated_sp,
        'updated_spareparts_copy':updated_sp_copy,
        'success': request.GET.get('success'),
        'error': request.GET.get('error')
    }
    return render(request,"Serviceman Templates/ListofUpdatedSparepart.html",context)


def remove_sparepart(request,spid_taskid):
    for i in spid_taskid:
        if i == ',':
            index = spid_taskid.index(i)

    sp_id = spid_taskid[0:index]
    task_id = spid_taskid[index+1::]
    sp_id = int(sp_id)
    task_id = int(task_id)
    updated_sp = Updated_Sparepart.objects.get(task_id=task_id,sparepart_id=sp_id)
    updated_sp.delete()
    messages.success(request, "Sparepart Removed Successfully...")
    return redirect('/view_updated_sp/{task_id}')
    # context = {
    #     'success':"Removed Successfully..."
    # }
    # query_string = urlencode(context)
    # redirected_url = f'/view_updated_sp/{task_id}?{query_string}'
    # return redirect(redirected_url)

def update_payment_to_user(request,task_id):
    s_id = request.session.get("serviceman_id")
    updated_sp = Updated_Sparepart.objects.filter(task_id=task_id)
    taskobj = Task.objects.get(id=task_id)
    if updated_sp:
        taskobj.need_sparepart=True
        taskobj.save()
    else:
        taskobj.need_sparepart = False
        taskobj.save()
    picked_task = Task.objects.filter(serviceman_id=s_id, status="Picked")
    for i in picked_task:
        try:
            spobj = Sparepart_payment.objects.get(task_id=i.id)
            if spobj:
                updatesp_button = True
        except:
            pass

    messages.success(request, "Payment Updated Successfuly...")
    return redirect('/picked_task')
    # context = {
    #     'success':"Payment Updated Successfuly..."
    # }
    # query_string = urlencode(context)
    # redirected_url = f'/picked_task?{query_string}'
    # return redirect(redirected_url)
    # return render(request,"Serviceman Templates/ServicemanTodayTask.html",context)



# For User Side
def sparepart_payment_summary_page(request,task_id):
    updated_sp = Updated_Sparepart.objects.filter(task_id=task_id)
    updated_sp_copy = Updated_Sparepart.objects.filter(task_id=task_id)
    amount = 0
    for i in updated_sp:
        if i.quantity != None:
            if i.quantity > 1:
                amount = amount + i.sparepart_id.sparepart_price * i.quantity
            else:
                amount = amount + i.sparepart_id.sparepart_price
        else:
            if i.square_feet != None:
                amount = amount + i.sparepart_id.sparepart_price * i.square_feet
            else:
                amount = amount + i.sparepart_id.sparepart_price

    tax = amount * 18 / 100
    tax = round(tax, 2)
    total = amount + tax
    total = round(total, 2)
    taskobj = Task.objects.get(id=task_id)
    catname = taskobj.booking_id.service_id.scatname.catname

    context={
        'catname':catname,
        'updated_spareparts':updated_sp,
        'updated_spareparts_copy':updated_sp_copy,
        'task_id':task_id,
        'total':total,
        'tax':tax,
    }
    return render(request,"User Templates/SparepartPaymentSummary.html",context)

def make_payment_for_updated_sparepart(request):
    u_id = request.session.get("user_id")
    task_id = request.POST.get("task_id")
    upi_id = request.POST.get("upi_id")
    tax = request.POST.get("tax")
    total = request.POST.get("total")
    taskobj = Task.objects.get(id=task_id)
    updated_sp = Updated_Sparepart.objects.filter(task_id=task_id)
    print(updated_sp)
    flag=0
    try:
        sp_payment_obj = Sparepart_payment.objects.get(task_id=task_id)
    except:
        flag=1

    if flag==0:
        sp_payment_obj = Sparepart_payment.objects.get(task_id=task_id)
        sp_payment_obj.sparepart_tax=tax
        sp_payment_obj.sparepart_total_amount=total
        sp_payment_obj.updated_spareparts.set(updated_sp)
        sp_payment_obj.booking_id=Booking(id=taskobj.booking_id.id)
        sp_payment_obj.task_id = Task(id=task_id)
        sp_payment_obj.upi_id = upi_id
        sp_payment_obj.save()
        for i in updated_sp:
            print(i.quantity)
            print(i.sparepart_id.sparepart_quantity)
            quantity = i.quantity
            sp_quantity = i.sparepart_id.sparepart_quantity
            if i.sparepart_id.sparepart_quantity != None:
                final = sp_quantity - quantity
                spobj = Sparepart.objects.get(id=i.sparepart_id.id)
                spobj.sparepart_quantity = final
                spobj.save()

        taskobj.need_sparepart=False
        taskobj.save()
    else:
        sp_payment_obj = Sparepart_payment.objects.create(task_id=Task(id=task_id),
                                                          sparepart_tax=tax,
                                                          sparepart_total_amount=total,
                                                          booking_id = Booking(id=taskobj.booking_id.id),
                                                          upi_id = upi_id)
        sp_payment_obj.updated_spareparts.set(updated_sp)
        sp_payment_obj.save()
        taskobj.need_sparepart = False
        taskobj.save()
        for i in updated_sp:
            print(i.quantity)
            print(i.sparepart_id.sparepart_quantity)
            quantity = i.quantity
            sp_quantity = i.sparepart_id.sparepart_quantity
            if i.sparepart_id.sparepart_quantity != None:
                final = sp_quantity - quantity
                spobj = Sparepart.objects.get(id=i.sparepart_id.id)
                spobj.sparepart_quantity = final
                spobj.save()

    context = {
        'sp_paymentobj':sp_payment_obj,
        # 'success': "Payment Done..."
    }
    messages.success(request, "Payment Done Successfully...")
    query_string = urlencode(context)
    redirected_url = f'/mybookings/On Going?{query_string}'
    return redirect(redirected_url)
    # return render(request, "User Templates/mybookings.html", context)