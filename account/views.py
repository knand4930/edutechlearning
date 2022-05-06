from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User
import uuid
from django.conf import settings
from django.core.mail import message, send_mail
from .helpers import send_forget_password_mail
from django.core.paginator import Paginator
from datetime import datetime, timedelta
# Create your views here.


def login_attempts(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username).first()

            if user_obj is None:
                messages.error(request, 'User Not Found')
                return redirect('login')

            profile_obj = Profile.objects.filter(user=user_obj).first()

            if not profile_obj.is_verified:
                messages.error(
                    request, 'profile is not verified please check your Email Address')
                return redirect('login')

            user = authenticate(username=username, password=password)

            if user is None:
                messages.error(request, 'Wrong Password')
                return redirect('login')

            login(request, user)
            return redirect('home')
    except Exception as e:
        print(e)
        messages.error(request,'please connect with admistrator !!')

    return render(request, 'login.html')


def register_attempts(request):
    try:
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
            mobile = request.POST.get('mobile')
            password = request.POST.get('password')

            try:
                if User.objects.filter(username=username).first():
                    messages.error(request, 'User Name Already Exists')
                    return redirect('signup')

                if User.objects.filter(email=email).first():
                    messages.error(request, 'Email Address already Exists')
                    return redirect('signup')
                if Profile.objects.filter(mobile=mobile).first():
                    messages.error(request, 'MObile Number already Exists')
                    return redirect('signup')
                user_obj = User.objects.create(
                    first_name=first_name, last_name=last_name, username=username, email=email)
                user_obj.set_password(password)
                user_obj.save()

                auth_token = str(uuid.uuid4())
                profile_obj = Profile.objects.create(
                    user=user_obj, auth_token=auth_token, name=first_name + '' + last_name, email=email, mobile=mobile)
                profile_obj.save()
                send_mail_after_registration(email, auth_token)
                return redirect('token_send')
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)
        messages.error(request, 'Please Connect with Admistrators !!')

    return render(request, 'registrations.html')


def success(request):
    return render(request, 'success.html')


def token_send(request):
    return render(request, 'token_send.html')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()
        if profile_obj:

            if profile_obj.is_verified:
                messages.success(
                    request, 'Your Account has been Alread verified')
                return redirect('signin')

            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(
                request, 'Congratulation , Your Account has been verified')
            return redirect('signin')

        else:
            return redirect('error')
    except Exception as e:
        print(e)
        return redirect('/')


def error_page(request):
    return render(request, 'error.html')


def send_mail_after_registration(email, token):
    subject = "Your Account Has Been Verified"
    message = f"Hello, Paste the link to verify your account https://educationora.com/verify/{token}"
    email_from = settings.EMAIL_HOST_USER
    recipients_list = [email]
    send_mail(subject, message, email_from, recipients_list)

#https://github.com/boxabhi/yotube_django_email.git


@csrf_exempt
def logout_view(request):
    if(request.user.is_authenticated is False):
        return redirect("login")
    logout(request)
    return redirect('login')


def changepassword(request, token):
    context = {}

    try:
        profile_obj = Profile.objects.filter(auth_token=token).first()
        context = {'user_id': profile_obj.user.id}

        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request, 'No user id found.')
                return redirect(f'/changepassword/{token}')

            if new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/changepassword/{token}')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('signin')

    except Exception as e:
        print(e)
    return render(request, 'changepassword.html', context)

#https://github.com/boxabhi/youtube_reset_password_django/blob/master/accounts/views.py


def forgetpassword(request):

    try:
        if request.method == 'POST':
            username = request.POST.get('username')

            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('forgetpassword')

            user_obj = User.objects.get(username=username)
            token = str(uuid.uuid4())
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.auth_token = token
            profile_obj.save()
            send_forget_password_mail(user_obj.email, token)
            messages.success(request, 'An email is sent.')
            return redirect('forgetpassword')

    except Exception as e:
        print(e)
        messages.error(request, "please connect with admistrator")
    return render(request, 'forgetpasswords.html')



def contactus(request):
    try:
        if request.method == 'POST':
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            sub = request.POST.get('sub')
            msg = request.POST.get('msg')
            data = ContactUs.objects.create(name=name, email=email, phone=phone,sub=sub, msg=msg)
            data.save()
            messages.success(request, 'Your Contact Details Has Been Submitted !!')
    except Exception as e:
        print(e)
        messages.error(request, 'Please connect with Admistrator !!')
    return render(request, 'contact.html')

def aboutus(request):
    abt = AboutUs.objects.all()
    return render(request, 'aboutus.html', {'abt': abt})