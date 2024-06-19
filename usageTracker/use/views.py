from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.db import IntegrityError
from django.db.models import Sum
from datetime import datetime
from .models import User, Usage

# Create your views here.
def register(request):

    # For get method
    if request.method == "GET":
        return render(request, "use/register.html")
    
    # For post method
    # Getting user name password and confirmation
    username = request.POST.get("username")
    password = request.POST.get("password")
    confirmation = request.POST.get("confirmation")

    if password != confirmation:
        return render(request, "user/register.html", {
            "message" : "Passwords do not match"
        })
    
    # Try to create a user
    try:
        user = User.objects.create_user(username=username, password=password)
        user.save()
    except IntegrityError:
        return render(request, "use/register.html", {
            "message" : "Username already taken"
        })
    
    # Login the user
    login(request, user)
    return HttpResponseRedirect(reverse("index"))


# For logging in
def login_view(request):

    # For get method
    if request.method == "GET":
        return render(request, "use/login.html")
    
    # For post method
    # Getting user name and password
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request, username=username, password=password)

    if user:
        # Login the user
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    return render(request, "use/login.html", {
        "message" : "Username doesn't exist"
    })

# For Loggin out
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))

# For Adding Usage
def add(request):
    if request.method == "GET":
        return render(request, "use/add.html")
    
    # For get method
    # Get cause and cost
    cause = request.POST.get("cause").title()
    cost = request.POST.get("cost")

    # Make sure that cost is indeed a number
    try:
        cost = float(cost)
    except ValueError:
        return render(request, "use/add.html", {
            "message" : "Cost must be a real number"
        })
    
    # getting current date
    today = datetime.now()

    
    # Create a usage object and save
    usage = Usage(user=request.user, cause=cause, cost=float(cost), day=today.day, month=today.month, year=today.year)
    usage.save()

    return HttpResponseRedirect(reverse("index"))

# For Checking usage
def index(request):

    # Get the usage for the current year and month
    today = datetime.now()

    # Getting total cost for each cause
    usages = Usage.objects.filter(user=request.user, year=today.year, month=today.month).values('cause').annotate(total_cost=Sum('cost'))

    # Getting total cost for all cause
    total_cost = Usage.objects.filter(user=request.user, year=today.year, month=today.month).aggregate(total=Sum("cost"))
    
    # Getting distinct year and month
    distinct_year_months = Usage.objects.values("year", "month").distinct()

    return render(request, "use/check.html", {
        "usages" : usages,
        "total_cost" : total_cost.get("total"),
        "dates" : distinct_year_months,
        "year" : today.year,
        "month" : today.month
    })

# For checking
def check(request, year, month):
    # Getting total cost for each cause
    usages = Usage.objects.filter(user=request.user, year=year, month=month).values('cause').annotate(total_cost=Sum('cost'))

    # Getting total cost for all cause
    total_cost = Usage.objects.filter(user=request.user, year=year, month=month).aggregate(total=Sum("cost"))
    
    # Getting distinct year and month
    distinct_year_months = Usage.objects.values("year", "month").distinct()

    return render(request, "use/check.html", {
        "usages" : usages,
        "total_cost" : total_cost.get("total"),
        "dates" : distinct_year_months,
        "year" : year,
        "month" : month
    })

# Look details usage
def details(request, year, month):

    # Get all the usage for that year and month order by day
    usages = Usage.objects.filter(year=year, month=month).order_by("day")

    return render(request, "use/details.html", {
        "usages" : usages
    })