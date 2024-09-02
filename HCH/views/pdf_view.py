from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.template.loader import get_template

from xhtml2pdf import pisa
from HCH.models.booking_model import Booking
from HCH.models.task_model import Task
from HCH.models.updated_sparepart_model import Updated_Sparepart
from HCH.models.sparepart_payment_model import Sparepart_payment
from HCH.models.payment_details_model import Paymentdetails
from HCH.models.service_man_model import Serviceman
from datetime import datetime,date
from django.contrib import messages

def report_page(request):
    context = 'f'
    return render(request, "PDF/ManagerReport.html")

def generate_report_by_date(request):
    memail = request.session.get("manager_email")
    if memail:
        Date = request.POST.get("date")
        # print("date format:", Date)
        bookings = Booking.objects.filter(booking_provide_date=Date)
        if bookings:
            tasks = Task.objects.all()
            updated_spareparts = Updated_Sparepart.objects.all()
            sp_payments = Sparepart_payment.objects.all()
            payments = Paymentdetails.objects.all()
            context = {
                'bookings':bookings,
                'tasks':tasks,
                'updated_spareparts':updated_spareparts,
                'sp_payments':sp_payments,
                'payments':payments
            }
            template_path = 'PDF/ManagerReport.html'

            response = HttpResponse(content_type='application/pdf')

            response['Content-Disposition'] = 'filename="Bookings_report.pdf"'

            template = get_template(template_path)

            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        else:
            messages.error(request, "No Any Record Found...")
            return redirect('/manager_dashboard')
            # servicemans = Serviceman.objects.all()
            # context = {
            #     'servicemans': servicemans,
            #     'error': "No Any Record Found..."
            # }
            # return render(request, "Manager Templates/ManagerDashboard.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def generate_report_by_month(request):
    memail = request.session.get("manager_email")
    if memail:
        month = request.POST.get("month")
        print("Month",month)
        # Date = '2024-03-27'
        # Date = datetime.strptime(Date, "%Y-%m-%d")
        # m = Date.strftime('%m')
        # y = Date.strftime('%Y')
        # my = str(y)+'-'+str(m)
        # print(my)
        bookingsobj = Booking.objects.all()
        bookings = []
        for i in bookingsobj:
            m = i.booking_provide_date.strftime('%m')
            y = i.booking_provide_date.strftime('%Y')
            my = str(y)+'-'+str(m)
            # print(my,' == ',month)
            if my == month:
                bookings.append(i)
        print(bookings)
        if bookings:
            tasks = Task.objects.all()
            updated_spareparts = Updated_Sparepart.objects.all()
            sp_payments = Sparepart_payment.objects.all()
            payments = Paymentdetails.objects.all()
            context = {
                'bookings': bookings,
                'tasks': tasks,
                'updated_spareparts': updated_spareparts,
                'sp_payments': sp_payments,
                'payments': payments,
            }
            template_path = 'PDF/ManagerReport.html'

            response = HttpResponse(content_type='application/pdf')

            response['Content-Disposition'] = 'filename="Bookings_report.pdf"'

            template = get_template(template_path)

            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        else:
            messages.error(request, "No Any Record Found...")
            return redirect('/manager_dashboard')
            # servicemans = Serviceman.objects.all()
            # context = {
            #     'servicemans': servicemans,
            #     'error': "No Any Record Found..."
            # }
            # return render(request, "Manager Templates/ManagerDashboard.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def generate_report_by_year(request):
    memail = request.session.get("manager_email")
    if memail:
        year = request.POST.get("year")
        print("Year:",year)
        # Date = '2024-03-27'
        # Date = datetime.strptime(Date, "%Y-%m-%d")
        # m = Date.strftime('%m')
        # y = Date.strftime('%Y')
        # my = str(y)+'-'+str(m)
        # print(my)
        bookingsobj = Booking.objects.all()
        bookings = []
        for i in bookingsobj:
            y = i.booking_provide_date.strftime('%Y')
            # print(my,' == ',month)
            if y == year:
                bookings.append(i)
        print(bookings)
        if bookings:
            tasks = Task.objects.all()
            updated_spareparts = Updated_Sparepart.objects.all()
            sp_payments = Sparepart_payment.objects.all()
            payments = Paymentdetails.objects.all()
            context = {
                'bookings': bookings,
                'tasks': tasks,
                'updated_spareparts': updated_spareparts,
                'sp_payments': sp_payments,
                'payments': payments,
            }
            template_path = 'PDF/ManagerReport.html'

            response = HttpResponse(content_type='application/pdf')

            response['Content-Disposition'] = 'filename="Bookings_report.pdf"'

            template = get_template(template_path)

            html = template.render(context)

            # create a pdf
            pisa_status = pisa.CreatePDF(
                html, dest=response)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        else:
            messages.error(request, "No Any Record Found...")
            return redirect('/manager_dashboard')
            # servicemans = Serviceman.objects.all()
            # context = {
            #     'servicemans': servicemans,
            #     'error': "No Any Record Found..."
            # }
            # return render(request, "Manager Templates/ManagerDashboard.html", context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")


def generate_invoice(request,booking_id):
    uemail = request.session.get("user_email")
    if uemail:
        booking_obj = Booking.objects.get(id=booking_id)
        catname = booking_obj.service_id.scatname.catname
        taskobj = Task.objects.get(booking_id=booking_id)
        today_date = date.today()
        payment_obj = Paymentdetails.objects.get(booking_id=booking_id)
        context = {}
        try:
            usp_obj = Updated_Sparepart.objects.filter(task_id=taskobj.id)
            sp_payment = Sparepart_payment.objects.get(task_id=taskobj.id)
            context.update({'updated_sp':usp_obj})
            context.update({'sp_payment':sp_payment})
        except:
            pass

        context.update({'booking_obj':booking_obj})
        context.update({'task_obj':taskobj})
        context.update({'today_date': today_date})
        context.update({'payment_obj':payment_obj})
        context.update({'catname':catname})
        template_path = 'PDF/Invoice.html'

        response = HttpResponse(content_type='application/pdf')

        response['Content-Disposition'] = 'filename="Bookings_report.pdf"'

        template = get_template(template_path)

        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
            html, dest=response)
        # if error then show some funy view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response
    else:
        return render(request, "Error Templates/LoginRequiredError.html")