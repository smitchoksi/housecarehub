from django.shortcuts import render, redirect

def serviceman_dashboard_page(request):
    semail = request.session.get("serviceman_email")
    if semail:
        return render(request, "Serviceman Templates/ServicemanDashboard.html")
    else:
        return render(request, "Error Templates/LoginRequiredError.html")