from __future__ import unicode_literals
from django.db import models
import datetime
import bcrypt
import re

class UserManager(models.Manager):
    def validate_registration(self,data):
        errors = {}
        # first name validation
        if len(data["name"]) < 3:
            errors["name"] = "Name must contain at least 3 characters"
        #elif not data["first_name"].isalpha():
            #errors["first_name"] = "First name must only contain letters"
        # last name validation
        if len(data["user_name"]) < 3:
            errors["user_name"] = "User name must contain at least 3 characters"
        #elif not data["last_name"].isalpha():
            #errors["last_name"] = "Last name must only contain letters"
        # email validation
        #email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        #if not email_regex.match(data["email"]):
            #errors["email"] ="Invalid Email Address!"
        # check if account already registered        
        elif User.objects.filter(user_name = data["user_name"]):
            errors["user_name"] = "An account already exists with that user name"
        # password validation
        if len(data["password"]) < 8:
            errors["password"] = "Password must be at least 8 characters long"
        elif data["password"] != data["cpassword"]:
            errors["password"] = "Password and confirm password must match"        
        # return either a user or an error
        if not errors:
            # ***************admin option************
            #if not User.objects.all():
            #    adminFlag = True
            #else:
            #    adminFlag = False
            # i would also need to add the admin flag when creating a user object: admin=adminFlag
            password = bcrypt.hashpw(data["password"].encode(), bcrypt.gensalt())
            user = User.objects.create(name=data["name"],user_name=data["user_name"],password=password)
            context = {"obj":user,"status":True}
            return context
        else:
            context = {"obj":errors,"status":False}
            return context
    
    def validate_login(self,data):
        errors = {"login": "could not login"}
        context = {"obj":errors,"status":False}
        user = User.objects.filter(user_name=data["user_name"])
        # user_name exists
        if user:
            # and password exists
            if bcrypt.checkpw(data["password"].encode(), user[0].password.encode()):
                context = {"obj":user[0],"status":True}
                return context
            # wrong password
            else:             
                return context
        # wrong email
        else:
            return context

class User(models.Model):
    name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # admin = models.BooleanField()
    objects = UserManager()

class TripManager(models.Manager):
    def validate(self, data):
        errors = {}
        # destination validation
        if len(data["destination"]) < 1:
            errors["destination"] = "Destination can't be empty"
        # description validation
        if len(data["description"]) < 1:
            errors["description"] = "Description can't be empty"
        # date validation
        if len(data["startdate"]) < 1:
            errors["startdate"] = "You must select a start date"
        if len(data["enddate"]) < 1:
            errors["enddate"] = "You must select an end date"
        if data["startdate"] and data["enddate"]:
            startdate = datetime.datetime.strptime(data["startdate"], "%Y-%m-%d")
            if  startdate < datetime.datetime.today() - datetime.timedelta(1):
                errors["startdate"] = "Start date has to be in the future"
            enddate = datetime.datetime.strptime(data["enddate"], "%Y-%m-%d")
            if  enddate < datetime.datetime.today() - datetime.timedelta(1):
                errors["enddate"] = "End date has to be in the future"
            if startdate > enddate:
                errors["date"] = "End date can't be before start date"
        # everything valid
        if not errors:
            user = User.objects.get(id=data["userid"])        
            trip = Trip.objects.create(destination=data["destination"],description=data["description"],start_date=startdate,end_date=enddate,planned_by=user)
            trip.save()
            trip.users_going.add(user)
            context = {"obj":trip,"status":True}
            return context
        else:
            context = {"obj":errors,"status":False}
            return context
        

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    planned_by = models.ForeignKey(User,related_name="planner")
    users_going = models.ManyToManyField(User,related_name="joined_trips")
    objects = TripManager()


