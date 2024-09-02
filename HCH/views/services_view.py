from django.shortcuts import render, redirect
from HCH.models.service_model import Service
from HCH.models.feedback_rating_model import Feedback_rating
import nltk
from nltk.tokenize import sent_tokenize
nltk.download('punkt')

def servicefun(request, subcat_id):
    #function call from Service model
    service_objects = Service.objects.filter(ssubcatname=subcat_id)
    for i in service_objects:
        print(i.sdescription)
        i.sdescription=sent_tokenize(i.sdescription)
    #print(service_objects)
    feedbackobj = Feedback_rating.objects.all()
    for i in service_objects:
        for j in feedbackobj:
            print(i.id, ' == ', j.service_id.id)
            if i.id == j.service_id.id:
                print(True)
    context ={
        'subcat_id':subcat_id,
        'services':service_objects,
        'feedbacks':feedbackobj
    }
    return render(request, "User Templates/servicepage.html", context)