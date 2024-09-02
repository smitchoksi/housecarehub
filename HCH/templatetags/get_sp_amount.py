from django import template

register = template.Library()

@register.filter(name="get_sparepart_amount")
def get_sp_amount_sqrfeet(price,x):
    if x==None:
        return price
    else:
        return price * x
