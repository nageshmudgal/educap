from django.shortcuts import render, redirect
from .models import Student,User_Otp
from adminmodule.models import Course,Notes
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
def homes(request):
    try:
        if request.session['studentuser'] != "":
            return redirect('../')
        else:
            return redirect('../')
    except:
        return redirect('../')


def signup(request):
   
    if request.method == 'GET':
        get_otp = request.GET['gotp']
        if get_otp:
            get_userid=request.GET['userid']
            user=Student.objects.get(id=get_userid)
            if int(get_otp) == User_Otp.objects.filter(user=user).last().otp :
                messages.success(request, "Account has been created")
                mess= f'Hello, {user.sname} \n your account has been successfully created \n Please wait for admin to active it. \n Thanks.'
                send_mail(
                "Welcome to Educap ",
                mess, 
                settings.EMAIL_HOST_USER,
                [user.semail],
                fail_silently = False

                )
                
                return redirect('../')
            else:
                messages.error(request, "You have entered wrong OTP")
                return render(request,'../student/otp.html',{'otp':True,'user':user})
    if request.method == 'POST':
        sname = request.POST['sname']
        semail = request.POST['semail']
        smobile = request.POST['smobile']
        password = request.POST['spassword']
        print(semail, password, sname, smobile)
        allemails = Student.objects.values_list("semail",flat=True)
        if semail in allemails:
            messages.warning(request, "Email is already registered")
            

        user = Student(sname=sname, semail=semail, smobile=smobile, password=password)
        user.save()
        user_opt=random.randint(100000,999999)

        User_Otp.objects.create(user=user,otp= user_opt)
        mess= f'Hello, {sname} \n your otp is {user_opt} \n Thanks.'
        send_mail(
            "Welcome to Educap - verify your email",
            mess, 
            settings.EMAIL_HOST_USER,
            [semail],
            fail_silently = False

        )
        return render(request,'otp.html',{'otp':True,'user':user})
        return redirect('../')
    return redirect('../')


def login(request):
    if request.method == "POST":
        e = request.POST['email']
        pas = request.POST['pas']
        try:
            user = Student.objects.get(semail=e, password=pas)
            if user.status=="Inactive":
                messages.warning(request, "Not Activated by Admin")
                return redirect("../")
            request.session['studentuser'] = user.id
            return redirect("../student/")
        except:
            return redirect("../")
    return redirect("../")


def logout(request):
    try:
        del request.session['studentuser']
        return redirect('../')
    except:
        return redirect("../")

def otp(request):
    return render(request,"otp.html")



import os
def profileupdate(request):
    try:
        if request.session['studentuser'] !="":
            user1 = Student.objects.get(id=request.session['studentuser'])
            if request.method == "POST":
                n = request.POST['name']
                e = request.POST['email']
                m = request.POST['mobile']
                i = request.FILES.get('imag')

                Student.objects.filter(id=request.session['studentuser']).update(sname=n)
                Student.objects.filter(id=request.session['studentuser']).update(semail=e)
                Student.objects.filter(id=request.session['studentuser']).update(smobile=m)
                if i:
                    image_path = user1.img.path
                    if os.path.exists(image_path):
                        os.remove(image_path)
                    
                    user1.img=i
                    user1.save()
            return redirect('../student')
        else:
            return redirect('../student')
    except:
        return redirect('../student')


def changepass(request):
    try:
        if request.session['studentuser'] !="":
            user1 = Student.objects.get(id=request.session['studentuser'])
            if request.method == "POST":
                pas1 = request.POST['pas1']
                pas2 = request.POST['pas2']
                print
                if pas1!=user1.password:
                    messages.warning(request,"old password isn't matching")
                    return redirect('../student')
                Student.objects.filter(id=request.session['studentuser']).update(password=pas2)
            return redirect('../student')
        else:
            return redirect('../student')
    except:
        return redirect('../student')