from django.shortcuts import render, redirect, HttpResponse
from datetime import datetime,date
from HCH.models.feedback_rating_model import Feedback_rating
from HCH.models.booking_model import Booking
from HCH.models.service_model import Service
from HCH.models.task_model import Task
from HCH.models.user_model import User
from urllib.parse import urlencode
from django.contrib import messages

def feedback_page(request,booking_id):
    uemail = request.session.get("user_email")
    if uemail:
        services = Service.objects.all()
        context = {
            'booking_id':booking_id,
            'services':services
        }
        return render(request,"User Templates/FeedbackForm.html",context)
    else:
        return render(request, "Error Templates/LoginRequiredError.html")

def submit_feedback(request):   # Form Submit Action URl
    uemail = request.session.get("user_email")
    if uemail:
        userobj = User.objects.get(u_email=uemail)
        if userobj.active:
            title = request.POST.get("title")
            description = request.POST.get("description")
            rating = request.POST.get("rating")
            booking_id = request.POST.get("booking_id")
            bookingobj = Booking.objects.get(id=booking_id)

            if rating==None:
                services = Service.objects.all()
                messages.error(request, "Please Give A Rating")
                context = {
                    # 'error':"Please Give A Rating",
                    'title':title,
                    'desc':description,
                    'booking_id':booking_id,
                    "services":services
                }
                return render(request, "User Templates/FeedbackForm.html",context)

            try:
                feedbackobj = Feedback_rating.objects.get(user_id=userobj.id, service_id=bookingobj.service_id.id)
                if feedbackobj:
                    rating = int(rating)
                    bookingobj = Booking.objects.get(id=booking_id)
                    todaytime = datetime.now()
                    feedbackobj.rating=rating
                    feedbackobj.feedback_title=title
                    feedbackobj.feedback_description=description
                    feedbackobj.feedback_datetime=todaytime
                    feedbackobj.user_id=User(id=bookingobj.user_id.id)
                    feedbackobj.service_id=Service(id=bookingobj.service_id.id)
                    feedbackobj.booking_id=Booking(id=bookingobj.id)
                    feedbackobj.save()
                    # context = {
                    #     'success': "Feedback Edited Successfully..."
                    # }
                    messages.success(request, "Feedback Edited Successfully...")
                    # query_string = urlencode(context)
                    # redirected_url = f'/?{query_string}'
                    return redirect("/")
            except:
                rating = int(rating)
                bookingobj = Booking.objects.get(id=booking_id)
                todaytime = datetime.now()
                feedback_data = Feedback_rating(rating=rating, feedback_title=title, feedback_description=description,
                                                feedback_datetime=todaytime, user_id=User(id=bookingobj.user_id.id),
                                                service_id=Service(id=bookingobj.service_id.id),
                                                booking_id=Booking(id=bookingobj.id))
                feedback_data.save()
                # context = {
                #     'success': "Feedback Submited Successfully...",
                # }
                messages.success(request, "Feedback Submited Successfully...")
                # query_string = urlencode(context)
                # redirected_url = f'/?{query_string}'
                return redirect("/")

        else:
            return HttpResponse('<h1>You Are Termite</h1>')
    else:
        return render(request, "Error Templates/LoginRequiredError.html")