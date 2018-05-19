from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *

def landing(request):
    return render(request, "beltexam_app/landing.html")

def register(request): 
    if request.method == "POST":
        # capture data
        request.session["name"] = request.POST["name"]
        request.session["user_name"] = request.POST["user_name"]  
        # validate data
        user = User.objects.validate_registration(request.POST)
        # if success add success msg to messages and redirect to profile
        if user["status"]:
            request.session["userid"] = user["obj"].id
            messages.success(request, "You've successfully registered!")
            return redirect("/success")
        # if errors add to messages and redirect back to landing page
        else:
            for value in user["obj"].values():
                messages.error(request, value)
            return redirect("/")
          
        return redirect("/")
    # if not post redirect to landing page
    return redirect("/")

def login(request):
    if request.method == "POST":
        #capture email
        request.session["user_name"] = request.POST["user_name"]    
        # validate
        user = User.objects.validate_login(request.POST)
        # if success add msg to success and redirect to profile
        if user["status"]:
            request.session["user_name"] = user["obj"].user_name
            request.session["userid"] = user["obj"].id
            messages.success(request, "You've successfully logged in!")
            return redirect("/success")
        # if errors add to messages and redirect back to landing page
        else:
            for value in user["obj"].values():
                messages.error(request, value)
            return redirect("/")
     # if not post redirect to landing page
    return redirect("/")    

def success(request):
    if not "user_name" in request.session:
        messages.error(request,"You must be logged in to access this page")
        return redirect('/')
    else:
        return redirect("/travels")

def logout(request):
    request.session.clear()
    messages.success(request,"Succesfully logged out!")
    return redirect('/')

def travels(request):
    if not "user_name" in request.session:
        messages.error(request,"You must be logged in to access this page")
        return redirect('/')
    user = User.objects.get(id=request.session["userid"])
    all_trips = Trip.objects.filter(users_going=user)
    others = Trip.objects.exclude(users_going=user)
    context = {"travels": all_trips, "others": others}
    return render(request, "beltexam_app/travels.html", context)

def travelsadd(request):
    if not "user_name" in request.session:
        messages.error(request,"You must be logged in to access this page")
        return redirect('/')
    return render(request, "beltexam_app/addtravel.html")

def travelsaddprocess(request):
    if request.method == "POST":
        # validate
        trip = Trip.objects.validate(request.POST)
        # if success add msg to success and redirect to profile
        if trip["status"]:
            #request.session["user_name"] = user["obj"].first_name
            #request.session["userid"] = user["obj"].id
            messages.success(request, "You've successfully added a trip!")
            return redirect("/travels")
        # if errors add to messages and redirect back to landing page
        else:
            for value in trip["obj"].values():
               messages.error(request, value)
            return redirect("/travels/add")
    # if not post redirect to landing page
    else:
        return redirect("/travels/add")

def destination(request, id):
    if not "user_name" in request.session:
        messages.error(request,"You must be logged in to access this page")
        return redirect('/')
    #user = User.objects.get(id=request.session["userid"])
    users_going = Trip.objects.get(id=id).users_going
    context = {"destination": Trip.objects.get(id=id),"others":users_going}
    return render(request, "beltexam_app/destination.html", context)

def jointrip(request):
    if request.method == "POST":
        # get curr user
        user = User.objects.get(id=request.session["userid"])
        # get trip
        trip = Trip.objects.get(id=request.POST["id"])
        # add travelers
        user.joined_trips.add(trip)
        messages.success(request, "You've successfully joined a trip!")
        return redirect("/travels")
    else:
        messages.error(request, "Could not join the trip")
        return redirect("/travels")