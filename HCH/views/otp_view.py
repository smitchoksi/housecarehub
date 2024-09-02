from django.shortcuts import render, redirect, HttpResponse
import random
from datetime import datetime,date
from django.core.mail import send_mail
from HCH.models.task_model import Task
from HCH.models.booking_model import Booking
from HCH.models.service_man_model import Serviceman
from HCH.models.sparepart_payment_model import Sparepart_payment
from datetime import datetime, timedelta
from urllib.parse import urlencode
from django.contrib import messages

def generate_otp():
    otp = ''.join(random.choices('0123456789', k=6))  # 6-digit OTP
    return otp

def send_otp_for_forgetpassword(request,uemail):
    try:
        request.session['OTP'] = generate_otp()
        request.session['Time'] = str(datetime.now())
        otp = request.session.get("OTP")
        subject = 'OTP For Forget Password'
        message = f'OTP is Valid For 5 Minutes, \n\nYOUR OTP IS: {otp}'
        from_email = 'housecarehub24@gmail.com'  # Sender's email
        to_email = uemail  # User's email
        send_mail(subject, message, from_email, [to_email])
    except:
        return render(request,"Error Templates/SomethingWentWrong.html")

def send_otp(request,task_id):
    semail = request.session.get("serviceman_email")
    if semail:
        taskobj = Task.objects.get(id=task_id)
        uemail = taskobj.booking_id.user_id
        # print("user email:",uemail)
        request.session['OTP']=generate_otp()
        request.session['Time']=str(datetime.now())
        otp = request.session.get("OTP")
        if taskobj.status == "Picked" and taskobj.start_time == None:
            send_otp_email_for_startwork(uemail, otp)
        elif taskobj.status == "Picked" and taskobj.start_time != None:
            send_otp_email_for_completework(uemail, otp)
        # context = {
        #     'success': "OTP Sended Successsfully..."
        # }
        messages.success(request, "OTP Sended Successsfully...")
        # query_string = urlencode(context)
        # redirected_url = f'/picked_task?{query_string}'
        return redirect('/picked_task')
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def send_otp_for_closetask(request,task_id):
    taskobj = Task.objects.get(id=task_id)
    s_id = request.session.get("serviceman_id")
    uemail = taskobj.booking_id.user_id
    # print("user email:",uemail)
    request.session['CLOSE_TASK_OTP']=generate_otp()
    request.session['Time']=str(datetime.now())
    otp = request.session.get("CLOSE_TASK_OTP")
    send_otp_email_for_closetask(uemail,otp)
    # context = {
    #     'success': "OTP Sended Successsfully..."
    # }
    messages.success(request, "OTP Sended Successsfully...")
    # query_string = urlencode(context)
    # redirected_url = f'/picked_task?{query_string}'
    return redirect('/picked_task')

def send_otp_email_for_startwork(user, otp):
    subject = 'OTP For Start Work Verification'
    message = f'If Our Serviceman is Reach At Your Home Only in This Case Share Your OTP To Service man, \nOTP is Valid For 5 Minutes, \n\nYOUR OTP IS: {otp}'
    from_email = 'housecarehub24@gmail.com'  # Sender's email
    to_email = user # User's email
    send_mail(subject, message, from_email, [to_email])


def send_otp_email_for_completework(user, otp):
    subject = 'OTP For Complete Work Verification'
    message = f'If Your Booked Service Work Completed Than Only Share This OTP To Serviceman, \nOTP is Valid For 5 Minutes, \n\nYOUR OTP IS: {otp}'
    from_email = 'housecarehub24@gmail.com'  # Sender's email
    to_email = user # User's email
    send_mail(subject, message, from_email, [to_email])

def send_otp_email_for_closetask(user, otp):
    subject = 'OTP For Close Work Verification'
    message = f'If You Agree For Close Booking Than Only Share This OTP To Serviceman, \nOTP is Valid For 5 Minutes, \n\nYOUR OTP IS: {otp}'
    from_email = 'krushanuinfolabz@gmail.com'  # Sender's email
    to_email = user # User's email
    send_mail(subject, message, from_email, [to_email])

def startwork_verify_otp_fun(request):
    semail = request.session.get("serviceman_email")
    if semail:
        request.session["spareparts"] = []
        otp = request.POST.get("otp")
        sendedopt = request.session.get("OTP")
        task_id = request.POST.get("task_id")
        time_session = request.session.get("Time")
        time_obj = datetime.strptime(time_session, "%Y-%m-%d %H:%M:%S.%f")
        # send_time = datetime.strptime(time_session, "%Y-%m-%d %H:%M:%S.%f")
        expire_time = time_obj + timedelta(minutes=5)
        flag = 0
        error_message = None
        if otp == sendedopt:
            pass
        else:
            flag = 1
            error_message = "Entered OTP is Wrong"

        if datetime.now() > expire_time:
            flag = 1
            error_message = "OTP is Expire"
            # print('Time Up')

        if flag and error_message != None:
            # context = {
            #     'error':error_message,
            # }
            messages.error(request, error_message)
            # query_string = urlencode(context)
            # redirected_url = f'/picked_task?{query_string}'
            return redirect('/picked_task')
        elif flag == 0 and error_message == None:
            taskobj = Task.objects.get(id=task_id)
            todaytime = datetime.now()
            taskobj.start_time = todaytime
            taskobj.save()
            # context = {
            #     'success': "OTP Verification Successsfully..."
            # }
            messages.success(request, "OTP Verification Successsfully...")
            # query_string = urlencode(context)
            # redirected_url = f'/picked_task?{query_string}'
            return redirect('/picked_task')
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def completework_verify_otp_fun(request):
    semail = request.session.get("serviceman_email")
    if semail:
        otp = request.POST.get("otp")
        sendedopt = request.session.get("OTP")
        task_id = request.POST.get("task_id")
        time_session = request.session.get("Time")
        time_obj = datetime.strptime(time_session, "%Y-%m-%d %H:%M:%S.%f")
        # send_time = datetime.strptime(time_session, "%Y-%m-%d %H:%M:%S.%f")
        expire_time = time_obj + timedelta(minutes=5)
        flag = 0
        error_message = None
        if otp == sendedopt:
            pass
        else:
            flag = 1
            error_message = "Entered OTP is Wrong"

        if datetime.now() > expire_time:
            flag = 1
            error_message = "OTP is Expire"
            # print('Time Up')

        if flag and error_message != None:
            # context = {
            #     'error':error_message,
            # }
            messages.error(request, error_message)
            # query_string = urlencode(context)
            # redirected_url = f'/picked_task?{query_string}'
            return redirect('/picked_task')
        elif flag == 0 and error_message == None:
            todaytime = datetime.now()
            taskobj = Task.objects.get(id=task_id)
            taskobj.status = "Completed"
            taskobj.complete_time = todaytime
            taskobj.need_sparepart = False
            taskobj.save()
            bookingobj = Booking.objects.get(id=taskobj.booking_id.id)
            bookingobj.booking_status = "Completed"
            bookingobj.save()
            servicemanobj = Serviceman.objects.get(id=taskobj.serviceman_id.id)
            servicemanobj.sm_status = "Available"
            servicemanobj.save()

            # context = {
            #     'success': "OTP Verification Successfully..."
            # }
            messages.success(request, "OTP Verification Successfully...")
            # query_string = urlencode(context)
            # redirected_url = f'/completed_task?{query_string}'
            return redirect('/completed_task')
            # return render(request, "Serviceman Templates/ServicemanTodayTask.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def closetask_verify_otp_fun(request):
    semail = request.session.get("serviceman_email")
    if semail:
        otp = request.POST.get("otp")
        sendedopt = request.session.get("CLOSE_TASK_OTP")
        task_id = request.POST.get("task_id")
        time_session = request.session.get("Time")
        time_obj = datetime.strptime(time_session, "%Y-%m-%d %H:%M:%S.%f")
        # send_time = datetime.strptime(time_session, "%Y-%m-%d %H:%M:%S.%f")
        expire_time = time_obj + timedelta(minutes=5)
        flag = 0
        error_message = None
        if otp == sendedopt:
            pass
        else:
            flag = 1
            error_message = "Entered OTP is Wrong"

        if datetime.now() > expire_time:
            flag = 1
            error_message = "OTP is Expire"
            print('Time Up')

        if flag and error_message != None:
            context = {
                'error':error_message,
            }
            messages.error(request, error_message)
            # query_string = urlencode(context)
            # redirected_url = f'/picked_task?{query_string}'
            return redirect('/picked_task')
        else:
            todaytime = datetime.now()
            taskobj = Task.objects.get(id=task_id)
            taskobj.status = "Closed"
            taskobj.close_task = todaytime
            taskobj.need_sparepart=False
            taskobj.save()
            bookingobj = Booking.objects.get(id=taskobj.booking_id.id)
            bookingobj.booking_status = "Completed"
            bookingobj.save()
            servicemanobj = Serviceman.objects.get(id=taskobj.serviceman_id.id)
            servicemanobj.sm_status = "Available"
            servicemanobj.save()

            # context = {
            #     'success': "OTP Verification Successfully..."
            # }
            messages.success(request, "OTP Verification Successfully...")
            # query_string = urlencode(context)
            # redirected_url = f'/completed_task?{query_string}'
            return redirect('/completed_task')
            # return render(request, "Serviceman Templates/ServicemanTodayTask.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")
