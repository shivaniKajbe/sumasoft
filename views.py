from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from soft.models import Profile
from datetime import datetime
from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return render(request,'index.html')

def login(request):
    return render(request,'login.html')

def add_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        hashed_password = make_password(password)
        user = User(username=username, password=hashed_password, email=email, first_name=first_name, last_name=last_name)
        user.save()

        return redirect('login')

    return render(request, 'add_user.html')

@login_required
def add_new_profile(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login')
    if request.method == 'POST':
        f = request.POST['first_name']
        l = request.POST['last_name']
        e = request.POST['email']
        p= request.POST['phone']
        a = request.POST['avatar']
        y = request.POST['years_of_experience']
        s = request.POST['skills']
        try:
            Profile.objects.create(first_name=f, last_name=l, email=e , phone=p, avatar=a, years_of_experience=y, skills=s)
            error='no'
        except:
            error='yes'
    d={'error':error}
    return render(request,'add_new_profile.html', d)

def back(request):
    return render(request, 'index.html')


def show_all_profile(request):
    profiles = Profile.objects.all()
    return render(request, 'show_all_profile.html', {'profiles': profiles})

def single_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    context = {
        'profile': profile,
    }
    return render(request, 'single_profile.html', context)

def update_profile(request, profile_id):
    profile = get_object_or_404(Profile, id=profile_id)
    error = ""
    if request.method == 'POST':
        profile.first_name = request.POST['first_name']
        profile.last_name = request.POST['last_name']
        profile.email = request.POST['email']
        profile.phone = request.POST['phone']
        profile.avatar = request.POST['avatar']
        profile.years_of_experience = request.POST['years_of_experience']
        profile.skills = request.POST['skills']
        try:
            profile.save()
            error = 'no'
        except:
            error = 'yes'
    d = {'profile': profile, 'error': error}
    return render(request, 'update_profile.html', d)





