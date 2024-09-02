from django.shortcuts import render, redirect,HttpResponse
from HCH.models.category_model import Category
from HCH.models.service_model import Service
from HCH.models.user_model import User
def indexfun(request):
    try:
        print("Index Function is called")
        print(request.GET.get('success'))
        # function call from Category model
        uemail = request.session.get("user_email")
        if uemail:
            userobj = User.objects.get(u_email=uemail)
            if userobj and userobj.active:
                category_objects = Category.get_all_category()
                services = Service.objects.all()
                context = {
                    'error':request.GET.get('error'),
                    'success':request.GET.get('success'),
                    'category': category_objects,
                    'services':services
                }
                return render(request,"User Templates/index.html",context)
            else:
                return HttpResponse("<h1>You Are Terminate</h1>")
        else:
            category_objects = Category.get_all_category()
            services = Service.objects.all()
            context = {
                'success': request.GET.get('success'),
                'category': category_objects,
                'services': services
            }
            return render(request, "User Templates/index.html", context)
    except:
        return render(request, "Error Templates/SomethingWentWrong.html")
