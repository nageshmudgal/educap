from django.shortcuts import render,redirect,HttpResponse
from .models import Admins,Course,Notes,Assignment,Video
from django.core.paginator import Paginator
from student.models import Student


def home(request):
    try:
        if request.session['userid'] != "":
            admin = Admins.objects.get(id=request.session['userid'])
            c = Course.objects.filter(status="active")
            n = Notes.objects.filter(status="active")
            a = Assignment.objects.filter(status="active")
            v = Video.objects.filter(status="active")

            params = {'courses': c,"notes":n,"assignments":a,"videos":v,"admin": admin}
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

def notes(request):
    if request.method == "POST":
        cid = request.POST['cid']
        name = request.POST['name']
        f = request.FILES.get('notes')
        print(f)
        c = Course.objects.get(id=cid)
        ins = Notes(cid=c, name=name, file=f)
        ins.save()
    return redirect("course")

def video(request):
    if request.method == "POST":
        cid = request.POST['cid']
        name = request.POST['name']
        f = request.FILES.get('video')
        print(name)
        c = Course.objects.get(id=cid)
        ins = Video(cid=c, name=name, file=f)
        ins.save()
    return redirect("course")


def editCourse(request):
    try:
        if request.session['userid'] !="":
            if request.method == "POST":
                cid = request.POST['cid']
                n = request.POST['name']
                d = request.POST['desc']
                
                Course.objects.filter(id=cid).update(name=n,desc=d)
            return redirect('../adminmodule/course')
        else:
            return redirect('../adminmodule')
    except:
        return redirect('../adminmodule')


def editassignment(request):
    try:
        if request.session['userid'] !="":
            if request.method == "POST":
                cid = request.POST['cid']
                n = request.POST['name']
                f = request.FILES.get('assignment')
                print(cid,n,f)
                Assignment.objects.filter(id=cid).update(name=n)
                ins = Assignment.objects.get(id=cid)
                ins.file=f
                ins.save()
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
def editNotes(request):
    try:
        if request.session['userid'] !="":
            if request.method == "POST":
                cid = request.POST['cid']
                n = request.POST['name']
                f = request.FILES.get('notes')
                print(cid,n,f)
                Notes.objects.filter(id=cid).update(name=n)
                
                ins = Notes.objects.get(id=cid)
                ins.file=f
                ins.save()
            return redirect('../adminmodule/course')
        else:
            return redirect('../adminmodule')
    except:
        return redirect('../adminmodule')

def editvideo(request):
    try:
        if request.session['userid'] !="":
            if request.method == "POST":
                cid = request.POST['cid']
                n = request.POST['name']
                f = request.FILES.get('video')
                print(cid,n,f)
                Video.objects.filter(id=cid).update(name=n)
                ins = Video.objects.get(id=cid)
                ins.file=f
                ins.save()
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
    if request.GET['op']=='2':
        b = request.GET['data']
        Notes.objects.filter(pk=b).update(status="deleted")
        return redirect('course')
    if request.GET['op']=='3':
        b = request.GET['data']
        Assignment.objects.filter(pk=b).update(status="deleted")
        return redirect('course')
    if request.GET['op']=='4':
        b = request.GET['data']
        Video.objects.filter(pk=b).update(status="deleted")
        return redirect('course')
    return HttpResponse("Error")


def showusers(request):
    try:
        if request.session['userid'] != "":
            user = Admins.objects.get(id=request.session['userid'])
            u = Student.objects.all()

            member_paginator = Paginator(u, 8)
            page_num = request.GET.get('page')
            page = member_paginator.get_page(page_num)

            return render(request, 'adminmodule/showusers.html', {"admin": user, "users": page})
        else:

            return redirect('../adminmodule/login')
    except:
        return redirect('../adminmodule/login')

def activateuser(request):
    try:
        if request.session['userid'] !="":
            b = request.GET['data']
            inactivebranch = Student.objects.get(pk=b)
            flag=0
            if inactivebranch.status=="Active":
                inactivebranch.status="Inactive"
                flag=1
            if inactivebranch.status=="Inactive" and flag==0:
                inactivebranch.status="Active"
            inactivebranch.save()
            return redirect('../adminmodule/showusers')
        else:
            return redirect('../adminmodule/login')
    except:
        return redirect('../adminmodule/login')