from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import profilepic
import subprocess

def index(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    else:
        return redirect('/signin')
    
def home(request):
    if request.user.is_authenticated:
        return render(request, "home.html")
    else:
        return redirect('/signin')

def signin(request):
    if request.user.is_authenticated:
        return redirect('/index')
    else:
        if request.method == "POST":
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/index')
            else:
                return render(request, "login.html", {"error": "Invalid credentials"})
        else:
            return render(request, "login.html")
        
def profile(request):
    if request.user.is_authenticated:
        return render(request, "profile.html")
    else:
        return redirect('/signin')

def gallery(request):
    if request.user.is_authenticated:
        pr = profilepic.objects.all().filter(user=request.user)
        c = {"img": pr}
        return render(request, "gallery.html", context=c)
    else:
        return redirect('/signin')

def tips(request):
    if request.user.is_authenticated:
        return render(request, "tips.html")
    
def signout(request):
    logout(request)
    return redirect('/signin')

def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confpassword = request.POST['confirmpassword']
        if password == confpassword:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('/index')
        else:
            return redirect('/signup')
    else:
        return render(request, 'signup.html')

def open_camera(request):
    if request.method == 'POST':
        try:
            result = subprocess.run(
                ["python", "virtual_paint.py"],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            return render(request, 'home.html')
        except subprocess.CalledProcessError as e:
            return HttpResponse(f"Error: {e.stderr}")
    return render(request, 'home.html')
@login_required
def upload(request):
    if request.method == "POST":
        pr = profilepic.objects.all().filter(user=request.user)
        # pr.delete()
        pic = request.FILES['pic']

        new = profilepic(user=request.user, pic=pic)
        new.save()
        return redirect('/gallery/')
    else:
        return redirect('/gallery')



def delete(request):
    if request.method == 'POST':
        pr = profilepic.objects.all().filter(user=request.user)
        pr.delete()
    return redirect('/gallery/')