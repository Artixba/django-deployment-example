from django.shortcuts import render
from basic_app.forms import UserForm, UserProfileInfoForm

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in Nice!")

@login_required #makes it so that the user has to be logged in in order to see logout. wouldn't make sense to see that if you're not logged in
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):

    registered=False #checks if user is registered

    if request.method =="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():

            user = user_form.save() # grabs user form from forms.py
            user.set_password(user.password) #This hashes the password
            user.save() #saves hashed password

            profile = profile_form.save(commit=False) # don't commit yet otherwise you risk of collisions
            profile.user = user # sets up 1 to 1 relationship

            if 'profile_pic' in request.FILES: # we use FILES since we deal with actual files
                profile.profile_pic = request.FILES['profile_pic'] # dictionary of all files they've uploaded

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors) # prints out form error
    else:
        user_form= UserForm()  # here is where the html error goes 
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/registration.html',
                            {'user_form':user_form,
                                'profile_form':profile_form,
                                'registered':registered}) 
    # In the braces, you pass in the context dictionary located in your registration.html

def user_login(request):

    if request.method == 'POST': #user filled login information
        username = request.POST.get('username') #grabs the name 'username from the login.html folder'
        password = request.POST.get('password')

        user = authenticate(username=username,password=password) # django's builtin password authentication function
        if user:
            if user.is_active: #checks if account is active
                login(request,user)
                return HttpResponseRedirect(reverse('index')) #the HTTPResponse redirects the user back to the homepage once logged in, reverse index essentially tells the website to go to that particular page.
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE") #if account is not active
        else:
            print("someone tried to login and failed!") # The print statements essentially get printed onto our console. Not recommended if you're working on an important site since this code is too direct.
            print("Username:{} and password{}".format(username,password))
            return HttpResponse("invalid login details supplied!")
    else:
        return render(request,'basic_app/login.html',{})
    