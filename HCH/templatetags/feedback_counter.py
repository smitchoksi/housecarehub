from django import template
from HCH.models.feedback_rating_model import Feedback_rating
register = template.Library()

@register.filter(name="FeedbackCounterFor_5Star")
def feedback_counter5(service_id):
    feedback_obj = Feedback_rating.objects.filter(service_id=service_id,rating=5)
    count = 0
    for i in feedback_obj:
        count = count+1
    return count

@register.filter(name="FeedbackCounterFor_4Star")
def feedback_counter4(service_id):
    feedback_obj = Feedback_rating.objects.filter(service_id=service_id,rating=4)
    count = 0
    for i in feedback_obj:
        count = count+1
    return count

@register.filter(name="FeedbackCounterFor_3Star")
def feedback_counter3(service_id):
    feedback_obj = Feedback_rating.objects.filter(service_id=service_id,rating=3)
    count = 0
    for i in feedback_obj:
        count = count+1
    return count

@register.filter(name="FeedbackCounterFor_2Star")
def feedback_counter2(service_id):
    feedback_obj = Feedback_rating.objects.filter(service_id=service_id,rating=2)
    count = 0
    for i in feedback_obj:
        count = count+1
    return count

@register.filter(name="FeedbackCounterFor_1Star")
def feedback_counter1(service_id):
    feedback_obj = Feedback_rating.objects.filter(service_id=service_id,rating=1)
    count = 0
    for i in feedback_obj:
        count = count+1
    return count
