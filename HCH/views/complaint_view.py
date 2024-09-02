from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from HCH.models.booking_model import Booking
from HCH.models.complaint_model import Complaint
from HCH.models.user_model import User
from HCH.models.service_model import Service
from urllib.parse import urlencode
from django.contrib import messages
from HCH.models.category_model import Category

def savecomplaintfun(request):      # Form Submit Action URl
    uemail = request.session.get("user_email")
    if uemail:
        b_id = request.POST.get("booking_id")
        topic = request.POST.get("complaint_topic")
        description = request.POST.get("complaint_desc")
        photo = request.POST.get("compaint_pic")

        data = {
            'booking_id':b_id,
            'complaint_topic':topic,
            'complaint_desc':description,
            'compaint_pic':photo
        }
        c_date = datetime.now()
        u_id = request.session.get("user_id")
        booking_data_obj = Booking.get_bookings_by_booking_id(b_id)


        if booking_data_obj:
            today = date.today()
            errormsg = None

            uemail = request.session.get("user_email")
            if uemail == booking_data_obj.user_id.u_email:

                if booking_data_obj.booking_status == "Completed":
                    bcompleted_date = booking_data_obj.booking_provide_date
                    sevendays = bcompleted_date + timedelta(days=7)
                    # print("booking complete date:", bcompleted_date)
                    # print("today:",today)
                    # print("After 7 days", sevendays)
                    if today>sevendays:
                        errormsg = "Your 7 days complaint policy is over"
                if booking_data_obj.booking_status == "Cancelled":
                    errormsg = "You can not submit complaint on cancelled booking"

                if errormsg == None:
                    serv_name = booking_data_obj.service_id
                    service_obj = Service.get_service_by_name(serv_name)
                    compaintdata = Complaint(complaint_date=c_date, complaint_topic=topic, complaint_pic=photo, complaint_description=description, user_id=User(id=u_id), booking_id=Booking(id=b_id), service_id=Service(id=service_obj.id))
                    compaintdata.save()
                    context = {
                        'success': "Your Complaint Submitted Successfully..."
                    }
                    query_string = urlencode(context)
                    redirected_url = f'/?{query_string}'
                    return redirect(redirected_url)
                else:
                    context = {}
                    context.update(data)
                    # context.update({'error': errormsg})
                    messages.error(request, errormsg)
                    query_string = urlencode(context)
                    redirected_url = f'/?{query_string}'
                    return redirect(redirected_url)
            else:
                errormsg = "Your Booking Id Is Not Valid";
                context = {}
                context.update(data)
                # context.update({'error':errormsg})
                messages.error(request, errormsg)
                query_string = urlencode(context)
                redirected_url = f'/?{query_string}'
                return redirect(redirected_url)
        else:
            errormsg = "Your Booking Id Is Not Valid";
            context = {}
            context.update(data)
            # context.update({'error': errormsg})
            messages.error(request, errormsg)
            query_string = urlencode(context)
            redirected_url = f'/?{query_string}'
            return redirect(redirected_url)

    else:
        return render(request, "Error Templates/LoginRequiredError.html")

