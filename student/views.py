from django.shortcuts import render, redirect
from .models import Student
from django.contrib import messages


# Create your views here.
def homes(request):
    try:
        if request.session['userid'] != "":
            return redirect('../')
        else:
            return redirect('../')
    except:
        return redirect('../')

def signup(request):
    if request.method == 'POST':
        sname = request.POST['sname']
        semail = request.POST['semail']
        smobile = request.POST['smobile']
        password = request.POST['spassword']
        print(semail, password, sname, smobile)
        user = Student(sname=sname, semail=semail, smobile=smobile, password=password)
        user.save()
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
            request.session['userid'] = user.id
            return redirect("../student/")
        except:
            return redirect("../")
    return redirect("../")


def logout(request):
    try:
        del request.session['userid']
        return redirect('../')
    except:
        return redirect("../")





import os
def profileupdate(request):
    try:
        if request.session['userid'] !="":
            user1 = Student.objects.get(id=request.session['userid'])
            if request.method == "POST":
                print("yes uesr")
                n = request.POST['name']
                e = request.POST['email']
                m = request.POST['mobile']
                print(n,e,m)
                Student.objects.filter(id=request.session['userid']).update(sname=n)
                Student.objects.filter(id=request.session['userid']).update(semail=e)
                Student.objects.filter(id=request.session['userid']).update(smobile=m)
                # if i:
                #     image_path = user1.img.path
                #     if os.path.exists(image_path):
                #         os.remove(image_path)
                #     user1.img=i
                #     user1.save()
            return redirect('../student')
        else:
            return redirect('../student')
    except:
        return redirect('../student')


def changepass(request):
    try:
        if request.session['userid'] !="":
            user1 = Student.objects.get(id=request.session['userid'])
            if request.method == "POST":
                pas1 = request.POST['pas1']
                pas2 = request.POST['pas2']
                print
                if pas1!=user1.password:
                    messages.warning(request,"old password isn't matching")
                    print("yeah")
                    return redirect('../student')
                Student.objects.filter(id=request.session['userid']).update(password=pas2)
            return redirect('../student')
        else:
            return redirect('../student')
    except:
        return redirect('../student')