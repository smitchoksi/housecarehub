from django.shortcuts import render, redirect,HttpResponse
from HCH.models.service_model import Service
from HCH.models.service_man_model import Serviceman
def search_service_result_fun(request):
    serviceobj = Service.objects.all()
    search = request.POST.get("search")
    print(search)
    for i in serviceobj:
        if search == i.sname:
            return redirect("servicepage/"+str(i.ssubcatname.id)+'#'+str(i.id))
            break
    else:
        services = Service.objects.all()
        context = {
            'services':services
        }
        return render(request,"Error Templates/SomethingWentWrong.html",context)


def search_serviceman_result_fun(request):
    servicemans = Serviceman.get_all_serviceman()
    search = request.POST.get("search")
    print(search)
    for i in servicemans:
        if search == i.sm_name:
            return redirect("/servicemanlistascategory"+'#'+str(i.id))
            break
    else:
        servicemans = Serviceman.get_all_serviceman()
        context = {
            'servicemans':servicemans
        }
        return render(request,"Error Templates/SomethingWentWrong(M).html",context)