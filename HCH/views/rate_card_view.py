from django.shortcuts import render, redirect
from HCH.models.sparepart_title_model import Spareparttitle
from HCH.models.subcategory_model import Subcategory
from HCH.models.sparepart_model import Sparepart
def rate_card(request,subcat_id):
    subcat_obj = Subcategory.objects.get(id=subcat_id)
    titles = Spareparttitle.objects.filter(sp_subcategory=subcat_obj)

    spobj = Sparepart.objects.all()
    spareparts = []
    for t in titles:
        for i in spobj:
            # print(t.id,'==',i.sparepart_title.id)
            if t.id == i.sparepart_title.id:
                spareparts.append(i)
                print(i.sparepart_name)
    print(spareparts)
    context = {
        'sp_titles':titles,
        'spareparts': spareparts
    }
    return render(request,"User Templates/Rate Card.html", context)