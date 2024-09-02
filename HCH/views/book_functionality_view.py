from django.shortcuts import render, redirect
from HCH.models.service_model import Service
from HCH.models.service_man_model import Serviceman
from HCH.models.user_model import User
from HCH.models.booking_model import Booking
from HCH.models.task_model import Task
from HCH.models.payment_details_model import Paymentdetails
from datetime import datetime, date, timedelta
from HCH.views.date_format import change_dateformat_as_fullmonth, change_dateformat_as_shortmonth
from urllib.parse import urlencode
from HCH.models.sparepart_payment_model import Sparepart_payment
from django.core.mail import send_mail
from django.contrib import messages
def get_payment_summery(sid):
    # print("sid", sid)
    service = Service.get_service_by_id(sid)

    # print("service id:",sid)
    # print("service list",service)
    service_price = service.sprice
    # print(service[0].sprice, service)
    service_tax = service_price * 18 / 100  # price * percentage / 100
    service_tax = round(service_tax, 2)
    service_total = service_price + service_tax
    service_total = round(service_total, 2)
    # print("price:", service_price, "tax:", service_tax)
    context = {
        'service_id':sid,
        'service_name': service.sname,
        'price': service_price,
        'tax': service_tax,
        'total': service_total
    }
    return context

def booknowpage(request,sid):
    #function call from Service model
    #print("booknow fun",sid)
    # print("function call first time")
    uemail = request.session.get("user_email")
    context = get_payment_summery(sid)
    services = Service.objects.all()
    context.update({'services':services})

    userobj = User.get_customer_by_id(uemail)

    # if customer login
    if userobj:
        f_name = userobj.u_fname
        l_name = userobj.u_lname
        name = f_name + " " + l_name
        phoneno = userobj.u_phoneno
        address = userobj.u_address
        area = userobj.u_area
        context.update({'name':name, 'contactno':phoneno,'address':address,'area':area})
        services = Service.objects.all()
        context.update({'services':services})
    return render(request, "User Templates/booknow.html", context)

def insertbookingdata(request):     # Form Submit Action URl
    uemail = request.session.get("user_email")
    if uemail:
        name= request.POST.get("name")
        contactno = request.POST.get("contactno")
        address = request.POST.get("address")
        area = request.POST.get("area")
        city = request.POST.get("city")
        state = request.POST.get("state")
        country = request.POST.get("country")

        # print("function call second time")
        service_id = request.POST.get("service_id")
        # print("Book done page service id:", service_id)
        services = Service.objects.all()
        booking_obj = Booking.objects.filter(booking_status="On Going")
        context = {
            'booking_obj':booking_obj,
            'name': name,
            'contactno': contactno,
            'address': address,
            'area': area,
            'city':city,
            'state':state,
            'country':country,
            'services':services
        }
        dates = Booking.fetchdates()
        context.update(dates)
        payment_summery = get_payment_summery(service_id)
        context.update(payment_summery)
        # print(context)

        if address=="None" or address==None:
            # context.update({'error':"Please Enter a Address"})
            messages.error(request, "Please Enter a Address")
            return render(request, "User Templates/booknow.html", context)

        if area=="None" or address==None:
            # context.update({'error': "Please Enter a Area"})
            messages.error(request, "Please Enter a Area")
            return render(request, "User Templates/booknow.html", context)

        return render(request, "User Templates/bookingdone.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def bookingdone(request):   # Form Submit Action URl
    uemail = request.session.get("user_email")
    if uemail:
        b_name = request.POST.get("name")
        b_contactno = request.POST.get("contactno")
        b_address = request.POST.get("address")
        b_area = request.POST.get("area")
        b_city = request.POST.get("city")
        b_state = request.POST.get("state")
        b_country = request.POST.get("country")
        b_provide_date = request.POST.get("booking_provide_date")
        b_provide_time = request.POST.get("booking_provide_time")
        service_id = request.POST.get("service_id")
        b_status = "On Going"
        upi_id = request.POST.get("upi_id")

        today = datetime.now()
        uid = request.session.get("user_id")
        try:
            b_provide_date = change_dateformat_as_fullmonth(b_provide_date)
        except:
            b_provide_date = change_dateformat_as_shortmonth(b_provide_date)

        bookings = Booking.objects.filter(booking_status="On Going", booking_provide_date=b_provide_date, booking_provide_time=b_provide_time, service_id=service_id)
        count = 0
        for i in bookings:
            count = count + 1
        print("Total",count,"Bookings")
        if count>=10:
            # error_message = f"Booking is full on {b_provide_date} {b_provide_time}"
            messages.error(request, f"Booking is full on {b_provide_date} {b_provide_time}")
            serviceobj = Service.objects.get(id=service_id)
            service_name = serviceobj.sname
            price = serviceobj.sprice
            tax = price * 18 / 100
            tax = round(tax, 2)
            total = price + tax
            total = round(total, 2)

            context = {
                # 'error':error_message,
                'name':b_name,
                'contactno':b_contactno,
                'address':b_address,
                'area':b_area,
                'city':b_city,
                'state':b_state,
                'country':b_country,
                'booking_provide_date':b_provide_date,
                'booking_provide_time':b_provide_time,
                'service_name':service_name,
                'service_id':service_id,
                'price':price,
                'tax':tax,
                'total':total
            }
            dates = Booking.fetchdates()
            context.update(dates)
            return render(request, "User Templates/bookingdone.html", context)
        else:
            booking_data = Booking(name=b_name,
                                   contactno=b_contactno,
                                   address=b_address,
                                   area=b_area,
                                   city=b_city,
                                   state=b_state,
                                   country=b_country,
                                   booking_date_time=today,
                                   booking_provide_date=b_provide_date,
                                   booking_provide_time=b_provide_time,
                                   booking_status=b_status,
                                   user_id=User(id=uid),
                                   service_id=Service(id=service_id))
            booking_data.save()
            task_data = Task(booking_id = Booking(id=booking_data.id))
            task_data.save()
            serviceobj = Service.objects.get(id=service_id)
            price = serviceobj.sprice
            tax = price * 18 / 100
            tax = round(tax, 2)
            total = price + tax
            total = round(total, 2)

            paymentdata = Paymentdetails(
                booking_id = Booking(id=booking_data.id),
                service_id=Service(id=service_id),
                user_id = User(id=uid),
                upi_id=upi_id,
                amount=price,
                tax = tax,
                totalamount=total)
            paymentdata.save()
            subject = 'Booking is Arrived'
            message = f'{serviceobj.sname} is booked by {uemail} Please Manage This Booking'
            from_email = 'housecarehub24@gmail.com'  # Sender's email
            to_email = "vrushal.pandav@gmail.com"  # Manager email
            send_mail(subject, message, from_email, [to_email])
            # context = {
            #     'success': "Booking Done Successfully"
            # }
            messages.success(request, "Booking Done Successfully")
            # query_string = urlencode(context)
            # redirected_url = f'/?{query_string}'
            return redirect("/")
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def mybookingpage(request, status):
    u_id = request.session.get("user_id")
    if u_id:
        # print(status)
        bookings = Booking.get_booking_by_status(u_id, status)
        bookings = bookings.order_by("-id")
        task = Task.objects.all()
        # print("Booking data:",bookings)
        services = Service.objects.all()
        context = {
            'task':task,
            'status':status,
            'bookings':bookings,
            'services':services,
            'sp_paymentobj': request.GET.get('sp_paymentobj'),
            'success': request.GET.get('success'),
            'error': request.GET.get('error'),
        }

        if status == "On Going":
            taskdata = Task.objects.all()
            services = Service.objects.all()
            context.update({'task':taskdata,'services':services})
        return render(request, "User Templates/mybookings.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def bookingdetailsfun(request, booking_id):
    uemail = request.session.get("user_email")
    if uemail:
        # print(booking_id)
        booking_obj = Booking.get_bookings_by_booking_id(booking_id)
        # print(booking_obj)
        taskobj = Task.objects.get(booking_id = booking_id)
        services = Service.objects.all()
        context = {
            'booking_obj':booking_obj,
            'task':taskobj,
            'services':services
        }
        try:
            spobj = Sparepart_payment.objects.get(task_id=taskobj.id)
            context.update({'sppayment':spobj})
            for i in spobj.updated_spareparts.all():
                print("Sparepart name:",spobj.updated_spareparts.all())
        except:
            pass

        paymentobj = Paymentdetails.objects.get(booking_id=booking_id)
        service_obj = Service.get_service_by_name(booking_obj.service_id)
        amount = paymentobj.amount
        tax = paymentobj.tax
        total = paymentobj.totalamount
        context.update({'service_obj':service_obj, 'amount':amount, 'tax':tax, 'total':total})
        return render(request,"User Templates/bookingdetails.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def cancelbookingfun(request,bookingid):
    taskobj = Task.objects.get(booking_id=bookingid)
    uemail = request.session.get("user_email")
    if uemail:
        if taskobj.status != "Picked":
            uemail = request.session.get("user_email")
            bookingobj = Booking.objects.get(id=bookingid)
            todaytime = datetime.now()
            bookingobj.booking_status="Cancelled"
            bookingobj.cancelledtime=todaytime
            bookingobj.save()
            if taskobj.serviceman_id != None:
                servicemanobj = Serviceman.objects.get(id = taskobj.serviceman_id.id)
                if servicemanobj:
                    servicemanobj.sm_status="Available"
                    servicemanobj.save()
            taskobj.serviceman_id=None
            taskobj.status="Cancelled"
            taskobj.assign_time=None
            taskobj.pick_time=None
            taskobj.save()
            paymentobj = Paymentdetails.objects.get(booking_id=bookingid)
            paymentobj.delete()
            # context = {
            #     'success': "Booking is Cancelled Successfully..."
            # }
            messages.success(request, "Booking is Cancelled Successfully...")
            # query_string = urlencode(context)
            # redirected_url = f'/?{query_string}'
            return redirect("/")
        else:
            return render(request,"Error Templates/error.html")
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

