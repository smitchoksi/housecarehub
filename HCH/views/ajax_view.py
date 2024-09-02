from django.http import JsonResponse
from HCH.models.sparepart_model import Sparepart
from HCH.models.sparepart_title_model import Spareparttitle
from HCH.models.task_model import Task

def fetch_spareparts(request,sptitle_id,task_id):
    taskobj = Task.objects.get(id=task_id)
    print("title:", sptitle_id)
    print("task obj:",taskobj.booking_id.service_id.ssubcatname)
    sp_titleobj = Spareparttitle.objects.get(id=sptitle_id, sp_subcategory=taskobj.booking_id.service_id.ssubcatname)
    spobj = Sparepart.objects.filter(sparepart_title=sp_titleobj.id)
    return JsonResponse({'sparepart':list(spobj.values())})