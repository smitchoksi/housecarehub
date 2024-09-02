from django import template
from HCH.models.feedback_rating_model import Feedback_rating
from django.db.models import Avg
register = template.Library()

@register.filter(name="FeedbackAverage")
def feedback_average(service_id):
    feedback_obj = Feedback_rating.objects.filter(service_id=service_id)
    average_rating = feedback_obj.aggregate(avg_rating=Avg('rating'))['avg_rating']
    if average_rating == None:
        return 0
    else:
        return average_rating

