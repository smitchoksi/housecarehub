from django.shortcuts import render, redirect
from datetime import datetime,date
from HCH.models.task_model import Task
from HCH.models.sparepart_payment_model import Sparepart_payment
from urllib.parse import urlencode
from django.contrib import messages

def task_history_fun(request):
    semail = request.session.get("serviceman_email")
    if semail:
        return render(request,"Serviceman Templates/ServicemanTaskHistory.html")
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def allocated_task_fun(request):
    semail = request.session.get("serviceman_email")
    if semail:
        s_id = request.session.get("serviceman_id")
        allocated_task = Task.objects.filter(serviceman_id=s_id, status="Allocated")
        flag=0
        updatesp_button = False
        if allocated_task:
            flag=1
        for i in allocated_task:
            try:
                spobj = Sparepart_payment.objects.get(task_id=i.id)
                if spobj:
                    updatesp_button = True
            except:
                pass

        context = {
            'tasks':allocated_task,
            'status':"Allocated",
            'flag':flag,
            'updatesp_button':updatesp_button
        }
        return render(request, "Serviceman Templates/ServicemanTodayTask.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def accept_task_fun(request,task_id):
    semail = request.session.get("serviceman_email")
    s_id = request.session.get("serviceman_id")
    if semail:
        taskobj = Task.objects.get(id=task_id)
        todaytime = datetime.now()
        taskobj.status = "Picked"
        taskobj.pick_time = todaytime
        taskobj.save()
        messages.success(request, "Task Accepted Successfully...")
        return redirect('/picked_task')
        # context = {
        #     'success':"Task Accepted Successfully..."
        # }
        # query_string = urlencode(context)
        # redirected_url = f'/picked_task?{query_string}'
        # return redirect(redirected_url)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def picked_task_fun(request):
    s_id = request.session.get("serviceman_id")
    if s_id:
        picked_task = Task.objects.filter(serviceman_id=s_id, status="Picked")
        flag=0
        updatesp_button = False
        if picked_task:
            flag=1
        for i in picked_task:
            try:
                spobj = Sparepart_payment.objects.get(task_id=i.id)
                if spobj:
                    updatesp_button = True
            except:
                pass

        context = {
            'error': request.GET.get('error'),
            'success': request.GET.get('success'),
            'tasks': picked_task,
            'flag':flag,
            'updatesp_button': updatesp_button
        }
        return render(request, "Serviceman Templates/ServicemanTodayTask.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

# def start_work_fun(request,task_id):
#     semail = request.session.get("serviceman_email")
#     if semail:
#         taskobj = Task.objects.get(id=task_id)
#         todaytime = datetime.now()
#         taskobj.start_time=todaytime
#         taskobj.save()
#         #return redirect('/picked_task')
#         s_id = request.session.get("serviceman_id")
#         picked_task = Task.objects.filter(serviceman_id=s_id, status="Picked")
#         updatesp_button = False
#         for i in picked_task:
#             try:
#                 spobj = Sparepart_payment.objects.get(task_id=i.id)
#                 if spobj:
#                     updatesp_button = True
#             except:
#                 pass
#         context = {
#             'tasks': picked_task,
#             'flag':1,
#             'updatesp_button':updatesp_button,
#             'success': "OTP Verification Successsfully..."
#         }
#         return render(request, "Serviceman Templates/ServicemanTodayTask.html", context)
#     else:
#         return render(request, "Error Templates/LoginRequiredError.html")
#
#
# def complete_work_fun(request,task_id):
#     semail = request.session.get("serviceman_email")
#     if semail:
#         todaytime = datetime.now()
#         taskobj = Task.objects.get(id=task_id)
#         taskobj.status = "Completed"
#         taskobj.complete_time = todaytime
#         taskobj.save()
#         bookingobj = Booking.objects.get(id=taskobj.booking_id.id)
#         bookingobj.booking_status="Completed"
#         bookingobj.save()
#         servicemanobj = Serviceman.objects.get(id=taskobj.serviceman_id.id)
#         servicemanobj.sm_status = "Available"
#         servicemanobj.save()
#         # return redirect('/competed_task')
#         s_id = request.session.get("serviceman_id")
#         completed_task = Task.objects.filter(serviceman_id=s_id, status="Completed")
#         context = {
#             'tasks': completed_task,
#             'flag': 1,
#             'success': "OTP Verification Successsfully..."
#         }
#         return render(request, "Serviceman Templates/ServicemanTodayTask.html", context)
#     else:
#         return render(request, "Error Templates/LoginRequiredError.html")
#
# def close_task_fun(request,task_id):
#     semail = request.session.get("serviceman_email")
#     if semail:
#         todaytime = datetime.now()
#         taskobj = Task.objects.get(id=task_id)
#         taskobj.status = "Closed"
#         taskobj.close_task = todaytime
#         taskobj.save()
#         bookingobj = Booking.objects.get(id=taskobj.booking_id.id)
#         bookingobj.booking_status="Completed"
#         bookingobj.save()
#         servicemanobj = Serviceman.objects.get(id=taskobj.serviceman_id.id)
#         servicemanobj.sm_status = "Available"
#         servicemanobj.save()
#         return redirect('/competed_task')
#     else:
#         return render(request, "Error Templates/LoginRequiredError.html")

def completed_task_fun(request):
    semail = request.session.get("serviceman_email")
    if semail:
        s_id = request.session.get("serviceman_id")
        todaydate = date.today()
        completed_task = Task.objects.filter(serviceman_id=s_id, status="Completed")
        completed_task_copy = Task.objects.filter(serviceman_id=s_id, status="Completed")
        flag = 0
        for i in completed_task:
            completedate = i.complete_time.date()
            if completedate == todaydate:
                flag = 1
                i.complete_time = completedate

        closed_task = Task.objects.filter(serviceman_id=s_id, status="Closed")
        closed_task_copy = Task.objects.filter(serviceman_id=s_id, status="Closed")

        if closed_task:
            for i in closed_task:
                closedate = i.close_task.date()

                if closedate == todaydate:
                    flag = 1
                    i.close_task = closedate

        context = {
                'error':request.GET.get('error'),
                'success': request.GET.get('success'),
                'flag':flag,
                'close_tasks':closed_task,
                'close_tasks_copy': closed_task_copy,
                'tasks':completed_task,
                'tasks_copy': completed_task_copy,
                'todaydate':todaydate
        }
        return render(request, "Serviceman Templates/ServicemanTodayTask.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def get_task_by_date(request):
    semail = request.session.get("serviceman_email")
    if semail:
        Date = request.POST.get("date")
        date_object = datetime.strptime(Date, "%Y-%m-%d")
        Date = date_object.strftime("%D")

        s_id = request.session.get("serviceman_id")
        completed_task = Task.objects.filter(serviceman_id=s_id, status="Completed")
        completed_task_copy = Task.objects.filter(serviceman_id=s_id, status="Completed")

        flag1 = 0
        for i in completed_task:
            completedate = i.complete_time.date()
            date_object = datetime.strptime(str(completedate), "%Y-%m-%d")
            completedate = date_object.strftime("%D")
            if completedate == Date:
                i.complete_time = completedate
                flag1=1

        closed_task = Task.objects.filter(serviceman_id=s_id, status="Closed")
        closed_task_copy = Task.objects.filter(serviceman_id=s_id, status="Closed")
        flag2 = 0
        for i in closed_task:
            closedate = i.close_task.date()
            date_object = datetime.strptime(str(closedate), "%Y-%m-%d")
            closedate = date_object.strftime("%D")
            if closedate == Date:
                i.close_task = closedate
                flag2 = 1

        context = {
            'closed_tasks':closed_task,
            'closed_tasks_copy': closed_task_copy,
            'tasks':completed_task,
            'tasks_copy': completed_task_copy,
            'date':Date,
            'flag1':flag1,
            'flag2': flag2

        }
        return render(request, "Serviceman Templates/ServicemanTaskHistory.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def get_task_by_month(request):
    semail = request.session.get("serviceman_email")
    if semail:
        monthyear = request.POST.get("monthyear")
        s_id = request.session.get("serviceman_id")
        completed_task = Task.objects.filter(serviceman_id=s_id, status="Completed")
        completed_task_copy = Task.objects.filter(serviceman_id=s_id, status="Completed")
        flag1 = 0
        for i in completed_task:
            completedate = str(i.complete_time.date())
            completedate = completedate[0:7]
            if completedate == monthyear:
                i.complete_time = completedate
                flag1 = 1

        closed_task = Task.objects.filter(serviceman_id=s_id, status="Closed")
        closed_task_copy = Task.objects.filter(serviceman_id=s_id, status="Closed")

        flag2 = 0
        for i in closed_task:
            closedate = str(i.close_task.date())
            closedate = closedate[0:7]
            if closedate == monthyear:
                i.close_task = closedate
                flag2 = 1

        context = {
            'closed_tasks':closed_task,
            'closed_task_copy':closed_task_copy,
            'tasks': completed_task,
            'tasks_copy': completed_task_copy,
            'date': monthyear,
            'flag1': flag1,
            'flag2': flag2
        }
        return render(request, "Serviceman Templates/ServicemanTaskHistory.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")
