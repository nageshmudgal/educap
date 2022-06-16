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
        # "notes":n,"assignments":a,"videos":v,
        params = {'course': c,"notes":n,"assignments":a,"videos":v, "admin": Admins.objects.get(id=request.session['userid'])}

        return render(request, 'adminmodule/viewcourse.html', params)

    except:
        return redirect('../adminmodule/login')

def assignment(request):
    if request.method == "POST":
        cid = request.POST['cid']
        name = request.POST['name']
        f = request.FILES.get('assignment')
        print(name)
        c = Course.objects.get(id=cid)
        ins = Assignment(cid=c, name=name, file=f)
        ins.save()
    return redirect("course")

def editassignment(request):
    try:
        if request.session['userid'] !="":
            if request.method == "POST":
                cid = request.POST['cid']
                n = request.POST['name']
                f = request.FILES.get('assignment')
                
                Assignment.objects.filter(id=cid).update(name=n)
                Assignment.objects.filter(id=cid).update(file=f)
                
                # if f:
                #     image_path = f.file.path
                #     if os.path.exists(image_path):
                #         os.remove(image_path)
                #     Assignment.objects.filter(id=cid).update(file=f)

            return redirect('../adminmodule/course')
        else:
            return redirect('../adminmodule')
    except:
        return redirect('../adminmodule')

def deleteinstance(request):
    if request.GET['op']=='1':
        b = request.GET['data']
        Course.objects.filter(pk=b).update(status="deleted")
        return redirect('course')
    return HttpResponse("Error")

