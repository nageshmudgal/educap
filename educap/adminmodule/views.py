from django.shortcuts import render,redirect,HttpResponse
from .models import Admins,Course,Notes,Assignment,Video
from django.core.paginator import Paginator


def home(request):
    try:
        if request.session['userid'] != "":
            admin = Admins.objects.get(id=request.session['userid'])

            params = {"admin": admin}
            return render(request, "adminmodule/home.html", params)
        else:
            return redirect('../adminmodule/login')
    except:
        return redirect('../adminmodule/login')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        pas = request.POST['pas']
        try:
            user = Admins.objects.get(email=email,password=pas)
            print(user)
            request.session['userid']=user.id
            return redirect("../adminmodule")
        except:
            return redirect("../adminmodule/login")

    return render(request,'adminmodule/login.html')

def logout(request):
    try:
        del request.session['userid']
        return redirect('../')
    except:
        return redirect("../adminmodule/login")


def course(request):
    try:

        if request.method == "POST":
            name = request.POST['name']
            d = request.POST['desc']
            ins = Course(name=name, desc=d)
            ins.save()

        courses = Course.objects.filter(status="active")

        member_paginator = Paginator(courses, 8)

        page_num = request.GET.get('page')

        page = member_paginator.get_page(page_num)

        params = {"courses": page, "admin": Admins.objects.get(id=request.session['userid'])}

        return render(request, 'adminmodule/course.html', params)
    except:
        return redirect('../adminmodule/login')

def viewcourse(request):
    try:
        data = request.GET['data']
        c = Course.objects.get(pk=data)
        n = Notes.objects.filter(cid=c,status="active")
        a = Assignment.objects.filter(cid=c, status="active")
        v = Video.objects.filter(cid=c, status="active")
        f = Video.objects.filter(cid=0, status="active")
        f=f.union(n,a,v)
        print(f)
        # "notes":n,"assignments":a,"videos":v,
        params = {'course': c,"files":f, "admin": Admins.objects.get(id=request.session['userid'])}

        return render(request, 'adminmodule/viewcourse.html', params)

    except:
        return redirect('../adminmodule/login')

def deleteinstance(request):
    if request.GET['op']=='1':
        b = request.GET['data']
        Course.objects.filter(pk=b).update(status="deleted")
        return redirect('course')

    return HttpResponse("Error")

