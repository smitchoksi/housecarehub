from .date_format import change_dateformat_as_shortmonth,change_dateformat_as_fullmonth, ChangeDateFormat

from django.shortcuts import render, redirect
from HCH.models.task_model import Task
from HCH.models.booking_model import Booking
from HCH.models.service_man_model import Serviceman
from HCH.models.sparepart_payment_model import Sparepart_payment
from HCH.models.payment_details_model import Paymentdetails
from HCH.models.updated_sparepart_model import Updated_Sparepart
from HCH.models.sparepart_model import Sparepart
from datetime import datetime,date
from urllib.parse import urlencode
from django.core.mail import send_mail
from django.contrib import messages
from HCH.models.service_model import Service


def get_formated_timeslot(timeslot):
    if timeslot == '0':
        timeslot = "All"
    elif timeslot == '1':
        timeslot = "10:00 AM"
    elif timeslot == '2':
        timeslot = "1:00 PM"
    elif timeslot == '3':
        timeslot = "4:00 PM"
    return timeslot

def reformate_timeslot(timeslot):
    if timeslot == "All":
        timeslot = '0'
    elif timeslot == "10:00 AM":
        timeslot = '1'
    elif timeslot == "1:00 PM":
        timeslot = '2'
    elif timeslot == "4:00 PM":
        timeslot = '3'
    return timeslot
def fetchdate(request,date):
    return print(date)

def task_list_fun(request):
    manager = request.session.get("manager_email")
    if manager:
        todaydate = date.today()
        servicemans = Serviceman.objects.all()
        context = {
            'date':todaydate,
            'temp':"0",
            'time':"All",
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def get_tasks_of_selected_date(request):
    manager = request.session.get("manager_email")
    if manager:
        Date = request.POST.get("date")
        timeslot = request.POST.get("timeslot")
        Time = get_formated_timeslot(timeslot)
        Date = ChangeDateFormat(str(Date))
        pending_tasks = Task.get_pending_task()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        servicemans = Serviceman.objects.all()
        context = {
            'task': pending_tasks,
            'date':Date,
            'temp':timeslot,
            'timeslot':Time,
            'servicemans':servicemans,
            'sparepart_payments': sparepart_payments,
            'service_payments': service_payments,
            'updated_spareparts': updated_spareparts
        }
        return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_all_task_by_date(request,DateTimeslot):
    manager = request.session.get("manager_email")
    if manager:
        Date = DateTimeslot[:-1]
        timeslot = DateTimeslot[-1]
        Time = get_formated_timeslot(timeslot)
        try:
            date_object = datetime.strptime(Date, "%b. %d, %Y").date()
        except:
            date_object = datetime.strptime(Date, "%B %d, %Y").date()

        tasks = Task.objects.all()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        servicemans = Serviceman.objects.all()
        context = {
            'task': tasks,
            'date': date_object,
            'temp': timeslot,
            'timeslot': Time,
            'servicemans':servicemans,
            'sparepart_payments':sparepart_payments,
            'service_payments':service_payments,
            'updated_spareparts':updated_spareparts
        }
        return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_pending_task_by_date(request,DateTimeslot):
    manager = request.session.get("manager_email")
    if manager:
        Date = DateTimeslot[:-1]
        timeslot = DateTimeslot[-1]
        Time = get_formated_timeslot(timeslot)
        try:
            date_object = datetime.strptime(Date, "%b. %d, %Y").date()
        except:
            date_object = datetime.strptime(Date, "%B %d, %Y").date()

        pending_tasks = Task.objects.filter(status="Pending")
        servicemans = Serviceman.objects.all()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        if request.GET.get('success'):
            context = {
                'task': pending_tasks,
                'date': date_object,
                'temp': timeslot,
                'timeslot': Time,
                'servicemans': servicemans,
                'sparepart_payments': sparepart_payments,
                'service_payments': service_payments,
                'updated_spareparts': updated_spareparts,
                'success': request.GET.get('success')
            }
            return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
        else:
            context = {
                'task': pending_tasks,
                'date': date_object,
                'temp': timeslot,
                'timeslot': Time,
                'servicemans': servicemans,
                'sparepart_payments': sparepart_payments,
                'service_payments': service_payments,
                'updated_spareparts': updated_spareparts
            }
            return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_allocated_task_by_date(request,DateTimeslot):
    manager = request.session.get("manager_email")
    if manager:
        Date = DateTimeslot[:-1]
        timeslot = DateTimeslot[-1]
        Time = get_formated_timeslot(timeslot)
        try:
            date_object = datetime.strptime(Date, "%b. %d, %Y").date()
        except:
            date_object = datetime.strptime(Date, "%B %d, %Y").date()

        alloctaed_tasks = Task.objects.filter(status="Allocated")
        servicemans = Serviceman.objects.all()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        if request.GET.get('success'):
            context = {
                'task': alloctaed_tasks,
                'date': date_object,
                'temp': timeslot,
                'timeslot': Time,
                'servicemans': servicemans,
                'sparepart_payments': sparepart_payments,
                'service_payments': service_payments,
                'updated_spareparts': updated_spareparts,
                'success': request.GET.get('success')

            }
            return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
        else:
            context = {
                'task': alloctaed_tasks,
                'date': date_object,
                'temp': timeslot,
                'timeslot': Time,
                'servicemans':servicemans,
                'sparepart_payments': sparepart_payments,
                'service_payments': service_payments,
                'updated_spareparts': updated_spareparts
            }
            return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_picked_task_by_date(request,DateTimeslot):
    manager = request.session.get("manager_email")
    if manager:
        Date = DateTimeslot[:-1]
        timeslot = DateTimeslot[-1]
        Time = get_formated_timeslot(timeslot)
        try:
            date_object = datetime.strptime(Date, "%b. %d, %Y").date()
        except:
            date_object = datetime.strptime(Date, "%B %d, %Y").date()

        pending_tasks = Task.objects.filter(status="Picked")
        servicemans = Serviceman.objects.all()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        context = {
            'task': pending_tasks,
            'date': date_object,
            'temp': timeslot,
            'timeslot': Time,
            'servicemans': servicemans,
            'sparepart_payments': sparepart_payments,
            'service_payments': service_payments,
            'updated_spareparts': updated_spareparts
        }
        return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_completed_task_by_date(request,DateTimeslot):
    manager = request.session.get("manager_email")
    if manager:
        Date = DateTimeslot[:-1]
        timeslot = DateTimeslot[-1]
        Time = get_formated_timeslot(timeslot)
        try:
            date_object = datetime.strptime(Date, "%b. %d, %Y").date()
        except:
            date_object = datetime.strptime(Date, "%B %d, %Y").date()

        pending_tasks = Task.objects.filter(status="Completed")
        servicemans = Serviceman.objects.all()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        context = {
            'task': pending_tasks,
            'date': date_object,
            'temp': timeslot,
            'timeslot': Time,
            'servicemans':servicemans,
            'sparepart_payments': sparepart_payments,
            'service_payments': service_payments,
            'updated_spareparts': updated_spareparts
        }
        return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_cancelled_task_by_date(request,DateTimeslot):
    manager = request.session.get("manager_email")
    if manager:
        Date = DateTimeslot[:-1]
        timeslot = DateTimeslot[-1]
        Time = get_formated_timeslot(timeslot)
        try:
            date_object = datetime.strptime(Date, "%b. %d, %Y").date()
        except:
            date_object = datetime.strptime(Date, "%B %d, %Y").date()

        canceled_tasks = Task.objects.filter(status="Cancelled")
        servicemans = Serviceman.objects.all()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        context = {
            'task': canceled_tasks,
            'date': date_object,
            'temp': timeslot,
            'timeslot': Time,
            'servicemans':servicemans,
            'sparepart_payments': sparepart_payments,
            'service_payments': service_payments,
            'updated_spareparts': updated_spareparts
        }
        return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_closed_task_by_date(request,DateTimeslot):
    manager = request.session.get("manager_email")
    if manager:
        Date = DateTimeslot[:-1]
        timeslot = DateTimeslot[-1]
        Time = get_formated_timeslot(timeslot)
        try:
            date_object = datetime.strptime(Date, "%b. %d, %Y").date()
        except:
            date_object = datetime.strptime(Date, "%B %d, %Y").date()

        closed_tasks = Task.objects.filter(status="Closed")
        servicemans = Serviceman.objects.all()
        sparepart_payments = Sparepart_payment.objects.all()
        service_payments = Paymentdetails.objects.all()
        updated_spareparts = Updated_Sparepart.objects.all()
        context = {
            'task': closed_tasks,
            'date': date_object,
            'temp': timeslot,
            'timeslot': Time,
            'servicemans':servicemans,
            'sparepart_payments': sparepart_payments,
            'service_payments': service_payments,
            'updated_spareparts': updated_spareparts
        }
        return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def fetch_serviceman_list_to_assigntask(request,catid_task_id):
    manager = request.session.get("manager_email")
    if manager:
        cat_id = int(catid_task_id[0])
        task_id = int(catid_task_id[1::])
        taskobj = Task.objects.get(id=task_id)
        subcategory = taskobj.booking_id.service_id.ssubcatname.id
        serviceman_obj = Serviceman.objects.filter(sm_Knowledge_of_category=cat_id, sm_knowledge_of_subcategory=subcategory, sm_status="Available",instaff=True)

        servicemans = Serviceman.objects.all()
        context = {
            'listofserviceman': serviceman_obj,
            'task_id':task_id,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/Servicemanlist_to_AssignTask.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def assign_task_to_serviceman(request,serviceman_id,task_id):
    manager = request.session.get("manager_email")
    if manager:
        todaytime = datetime.now()
        taskobj = Task.objects.get(id=task_id)
        taskobj.status="Allocated"
        taskobj.assign_time=todaytime
        taskobj.serviceman_id=Serviceman(id=serviceman_id)
        taskobj.save()
        servicemanobj = Serviceman.objects.get(id=serviceman_id)
        servicemanobj.sm_status="Allocated"
        servicemanobj.save()

        taskobj = Task.get_task_by_task_id(task_id)
        Date = taskobj.booking_id.booking_provide_date
        year, month, day = str(Date).split("-")
        month_names = {
            "01": "Jan",
            "02": "Feb",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "Aug",
            "09": "Sept",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec"
        }
        month_name = month_names[month]
        formatted_date = f"{month_name} {day}, {year}"
        timeslot = taskobj.booking_id.booking_provide_time
        timeslot = reformate_timeslot(timeslot)

        bookingobj = Booking.objects.get(id=taskobj.booking_id.id)
        service_name = bookingobj.service_id.sname
        subject = 'Task is Arrived'
        message = f'{service_name} is Allocated To You Please Complete It.'
        from_email = 'housecarehub24@gmail.com'  # Sender's email
        to_email = "vrushal.pandav@gmail.com"  # Serviceman email
        send_mail(subject, message, from_email, [to_email])
        # context = {
        #     'success':"Task Assigned Successfully...",
        # }
        # print(formatted_date)
        # query_string = urlencode(context)
        messages.success(request, "Task Assigned Successfully...")
        redirected_url = f'/listof_pendingtask_bydate/{formatted_date}{timeslot}'
        return redirect(redirected_url)
        # return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def retrieve_task(request,task_id):
    manager = request.session.get("manager_email")
    if manager:
        taskobj = Task.objects.get(id=task_id)
        servicemanobj = Serviceman.objects.get(id=taskobj.serviceman_id.id)
        servicemanobj.sm_status = "Available"
        servicemanobj.save()
        taskobj.serviceman_id=None
        taskobj.status="Pending"
        taskobj.assign_time = None
        taskobj.pick_time = None
        taskobj.start_time = None
        taskobj.need_sparepart=False
        taskobj.save()
        try:
            updated_sp = Updated_Sparepart.objects.filter(task_id=task_id)
            for i in updated_sp:
                quantity = i.quantity
                sp_quantity = i.sparepart_id.sparepart_quantity
                if i.sparepart_id.sparepart_quantity != None:
                    final = sp_quantity + quantity
                    spobj = Sparepart.objects.get(id=i.sparepart_id.id)
                    spobj.sparepart_quantity = final
                    spobj.save()
                updated_sp.delete()
        except:
            pass

        try:
            sp_payment_obj = Sparepart_payment.objects.get(task_id=task_id)
            sp_payment_obj.delete()
        except:
            pass
        Date = taskobj.booking_id.booking_provide_date
        year, month, day = str(Date).split("-")
        month_names = {
            "01": "Jan",
            "02": "Feb",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "Aug",
            "09": "Sept",
            "10": "Oct",
            "11": "Nov",
            "12": "Dec"
        }
        month_name = month_names[month]
        formatted_date = f"{month_name} {day}, {year}"
        timeslot = taskobj.booking_id.booking_provide_time
        timeslot = reformate_timeslot(timeslot)
        messages.success(request, "Task Retrieve Successfully...")
        # context = {
        #     'success': "Task Retrieve Successfully...",
        # }
        # query_string = urlencode(context)
        redirected_url = f'/listof_allocatedtask_bydate/{formatted_date}{timeslot}'
        return redirect(redirected_url)
        # return render(request, "Manager Templates/ListOfTask_of_SelectedDate.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_servicemantask_page(request,s_id):
    manager = request.session.get("manager_email")
    if manager:
        servicemanobj = Serviceman.objects.get(id=int(s_id))
        servicemans = Serviceman.objects.all()
        context = {
            'serviceman_id':s_id,
            'servicemanobj':servicemanobj,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/Task List.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def fetch_serviceman_tasklist_by_date(request):
    manager = request.session.get("manager_email")
    if manager:
        s_id = request.POST.get("serviceman_id")
        servicemanobj = Serviceman.objects.get(id=int(s_id))
        Date = request.POST.get("date")
        date_object = datetime.strptime(Date, "%Y-%m-%d")
        Date = date_object.strftime("%D")
        completed_tasks = Task.objects.filter(serviceman_id=s_id,status="Completed")
        completed_tasks_copy = Task.objects.filter(serviceman_id=s_id,status="Completed")
        flag = 0
        for i in completed_tasks:
            if i.complete_time != None:
                completedate = i.complete_time.date()
                date_object = datetime.strptime(str(completedate), "%Y-%m-%d")
                completedate = date_object.strftime("%D")
                if completedate == Date:
                    flag = 1
                    i.complete_time = completedate

        closed_tasks = Task.objects.filter(serviceman_id=s_id, status="Closed")
        closed_tasks_copy = Task.objects.filter(serviceman_id=s_id, status="Closed")
        for i in closed_tasks:
            if i.close_task != None:
                closedate = i.close_task.date()
                date_object = datetime.strptime(str(closedate), "%Y-%m-%d")
                closedate = date_object.strftime("%D")
                if closedate == Date:
                    flag = 1
                    i.close_task = closedate

        servicemans = Serviceman.objects.all()
        context = {
            'servicemanobj':servicemanobj,
            'completed_tasks':completed_tasks,
            'completed_tasks_copy':completed_tasks_copy,
            'closed_tasks':closed_tasks,
            'closed_tasks_copy':closed_tasks_copy,
            'flag':flag,
            'monthyear':Date,
            'serviceman_id':s_id,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/Task List.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def fetch_serviceman_tasklist_by_month(request):
    manager = request.session.get("manager_email")
    if manager:
        monthyear = request.POST.get("monthyear")
        s_id = request.POST.get("serviceman_id")
        servicemanobj = Serviceman.objects.get(id=int(s_id))
        completed_tasks = Task.objects.filter(serviceman_id=s_id,status="Completed")
        completed_tasks_copy = Task.objects.filter(serviceman_id=s_id,status="Completed")
        flag = 0
        for i in completed_tasks:
            if i.complete_time != None:
                completedate = str(i.complete_time.date())
                completedate = completedate[0:7]
                if completedate == monthyear:
                    flag = 1
                    i.complete_time = completedate

        closed_tasks = Task.objects.filter(serviceman_id=s_id, status="Closed")
        closed_tasks_copy = Task.objects.filter(serviceman_id=s_id, status="Closed")
        for i in closed_tasks:
            if i.close_task != None:
                closedate = str(i.close_task.date())
                closedate = closedate[0:7]
                if closedate == monthyear:
                    flag = 1
                    i.close_task = closedate

        servicemans = Serviceman.objects.all()
        context = {
            'servicemanobj':servicemanobj,
            'completed_tasks':completed_tasks,
            'completed_tasks_copy':completed_tasks_copy,
            'closed_tasks':closed_tasks,
            'closed_tasks_copy':closed_tasks_copy,
            'flag':flag,
            'monthyear':monthyear,
            'serviceman_id':s_id,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/Task List.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def list_of_all_task_page(request):
    manager = request.session.get("manager_email")
    if manager:
        servicemans = Serviceman.objects.all()
        context={
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/List Of All Task.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def fetch_list_of_all_task_by_date(request):
    manager = request.session.get("manager_email")
    if manager:
        Date = request.POST.get("date")
        # date_object = datetime.strptime(str(Date), "%Y-%m-%d")
        # print("Date:",Date)
        # print("date object:",date_object)
        bookingobj = Booking.objects.filter(booking_provide_date=Date)
        flag = 0
        if bookingobj:
            flag = 1
        taskobj = Task.objects.all()
        servicemans = Serviceman.objects.all()
        context = {
            'bookings':bookingobj,
            'tasks':taskobj,
            'date':Date,
            'flag':flag,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/List Of All Task.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def fetch_list_of_all_task_by_month(request):
    manager = request.session.get("manager_email")
    if manager:
        monthfilter = 1
        monthyear = request.POST.get("monthyear")
        # date_object = datetime.strptime(str(Date), "%Y-%m-%d")
        bookingobj = Booking.objects.all()
        bookingobj_copy = Booking.objects.all()
        taskobj = Task.objects.all()

        flag = 0
        for i in bookingobj:
            providedate = str(i.booking_provide_date)
            providedate = providedate[0:7]
            if providedate == monthyear:
                flag=1
                i.booking_provide_date = providedate

        servicemans = Serviceman.objects.all()
        context = {
            'bookings':bookingobj,
            'bookings_copy':bookingobj_copy,
            'tasks':taskobj,
            'date':monthyear,
            'flag':flag,
            'monthfilter':monthfilter,
            'servicemans':servicemans
        }
        return render(request, "Manager Templates/List Of All Task.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

