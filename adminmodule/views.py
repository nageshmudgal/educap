from django.shortcuts import render,redirect,HttpResponse
from .models import Admins,Course,Notes,Assignment,Video,Batch,Batch_videos
from django.core.paginator import Paginator
from django.contrib import messages
from student.models import Student
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q


def home(request):
    try:
        if request.session['userid'] != "":
            admin = Admins.objects.get(id=request.session['userid'])
            c = Course.objects.filter(status="active")
            n = Notes.objects.filter(status="active")
            a = Assignment.objects.filter(status="active")
            v = Video.objects.filter(status="active")
            s = Student.objects.filter(Q(status="Active") | Q(status="Inactive"))

            params = {'courses': c,"notes":n,"assignments":a,"videos":v,"admin": admin,"students":s}
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
            request.session['entry']=5
            return redirect("../adminmodule")
        except:
            return redirect("../adminmodule/login")

    return render(request,'adminmodule/login.html')

def logout(request):
    try:
        del request.session['userid']
        del request.session['entry']
        
        return redirect('../')
    except:
        return redirect("../adminmodule/login")

def course(request):
    # try:
        if request.method == "POST":
            name = request.POST['name']
            d = request.POST['desc']
            ins = Course(name=name, desc=d)
            print(ins)
            ins.save()

        f = request.GET.get('f')
        if f=='1':
            courses = Course.objects.filter(status="active").order_by('name')
        elif f:
            if len(f)>20:
                courses = Course.objects.none()
            else:
                courses= Course.objects.filter(name__icontains=f)
                
            if courses.count()==0:
                messages.warning(request, "No search results found. Please refine your query.")    
                return redirect('course')
        else:
            courses = Course.objects.filter(status="active")

        batches = Batch.objects.filter(status="active")

        
        en = request.GET.get('entry')
        if en:
            request.session['entry']= int(en)
        
        member_paginator = Paginator(courses, request.session['entry'])

        page_num = request.GET.get('page')

        page = member_paginator.get_page(page_num)

        params = {"batches": batches ,"courses": page, "admin": Admins.objects.get(id=request.session['userid'])}

        return render(request, 'adminmodule/course.html', params)
    # except:
        # return redirect('../adminmodule/login')

def Batches(request):
    # days=['mon','tues','wed','thrus','fri','sat','sun']
    if request.method=='POST':
        am=request.POST['a']
        id=request.POST['courses']
        days=request.POST.getlist('days')
        date=request.POST['date']
        time=request.POST['time']
        a=' '.join(days)
        c = Course.objects.get(id=id)
        ins = Batch(cid=c,days=a,date=date,time=time,a=am)
        print(ins)
        ins.save()
        return redirect('course')
    return redirect('course') 
   
def batchcontent(request):
    data=request.GET['data']
    
    b = Batch.objects.get(id=data,status="active")
    v = Batch_videos.objects.filter(bid=b,status="active")
    return render(request, 'adminmodule/batchcontent.html',{'b':b ,'v':v,"admin": Admins.objects.get(id=request.session['userid'])})

def batchvideo(request):
    if request.method == "POST":
        id = request.POST['bid']
        name = request.POST['names']
        f = request.FILES.get('video')
        print(id,name,f)
        b = Batch.objects.get(id=id,status="active")
        ins=Batch_videos(bid=b, name=name, file=f)
        ins.save()
        return redirect("viewbatch")
    return redirect("Batches")

def viewbatch(request):
    courses = Course.objects.filter(status="active")
    batch = Batch.objects.filter(status="active")
    view =  Batch_videos.objects.filter(status="active")
   
    f = request.GET.get('f')
    # print(f)
    if   f=='1':
                u = Batch.objects.filter(status="active").order_by('cid')  
                print(u)      
    elif f=='2':
                u =  Batch.objects.filter(~Q(status="deleted")).order_by('days')
                print(u)         
    elif f=='3':
                u =  Batch.objects.filter(~Q(status="deleted")).order_by('-date')  
                print(u) 
    elif f:                                                                         # search
            if len(f)>20:
                u = Batch.objects.none()
            else:
                allcourseName= Course.objects.filter(name__icontains=f).filter(~Q(status="deleted"))
                allbatchesname = Batch.objects.none()
                for i in allcourseName:
                    temp = Batch.objects.filter(cid=i)
                    allbatchesname = allbatchesname.union(temp)

                allbatchesdays= Batch.objects.filter(days__icontains=f).filter(~Q(status="deleted"))
                u = allbatchesname.union(allbatchesdays)
                
                    # if u.count()==0:
                    #     messages.warning(request, "No search results found. Please refine your query.")
    
    elif request.GET.getlist('selectedCourseFilter'):                               # Coursewise filter

        filterlist = request.GET.getlist('selectedCourseFilter')
        if "Deleted" in filterlist:
            u = Batch.objects.filter(status="deleted")
            filterlist.remove("Deleted")
        else:
            u = Batch.objects.all()
        
        for i in filterlist:
            co = Course.objects.get(id=i)
            temp = Batch.objects.filter(cid=co)
            u = u & temp
    else:
        u = Batch.objects.filter(status="active")      
    
    Batch_paginator = Paginator(u, request.session['entry'])
    page_num = request.GET.get('page')
    Batch_page = Batch_paginator.get_page(page_num)
    print(Batch.objects.get(id=11).date)

    params = {"batch": Batch_page,'course': courses ,"view":view ,"admin": Admins.objects.get(id=request.session['userid'])}
    return render(request, 'adminmodule/viewbatch.html', params)

def editbatch(request):
    if request.method=='POST':
        am=request.POST['a']
        id=request.POST['courses']
        days=request.POST.getlist('days')
        date=request.POST['date']
        time=request.POST['time']
        print(date)
        a=' '.join(days)
        print(a)
        c = Course.objects.get(id=id)
        Batch.objects.filter(cid=c).update(cid=c,days=a,date=date,time=time,a=am)
        b = Batch.objects.get(cid=c)
        print(b.date)

        
        return redirect("viewbatch")

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

def editBatchvideo(request):
    try:
        if request.session['userid'] !="":
            if request.method == "POST":
                cid = request.POST['bid']
                n = request.POST['name']
                f = request.FILES.get('video')
                print(cid,n,f)
                Batch.objects.filter(id=cid).update(name=n)
                ins = Batch_videos.objects.get(id=cid)
                ins.file=f
                ins.save()
            return redirect("Batches")
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
    if request.GET['op']=='5':
        b = request.GET['data']
        Batch.objects.filter(pk=b).update(status="deleted")
        return redirect('viewbatch')
    if request.GET['op']=='6':
        b = request.GET['data']
        Student.objects.filter(pk=b).update(status="deleted")
    if request.GET['op']=='7':
        b = request.GET['data']
        Batch_videos.objects.filter(pk=b).update(status="deleted")
        return redirect('Batches')
    return HttpResponse("Error")

def showusers(request):
    try:
        if request.session['userid'] != "":
            user = Admins.objects.get(id=request.session['userid'])
            c = Course.objects.filter(status="active")
            bat = Batch.objects.filter(status="active")

            
            f = request.GET.get('f')
            if f=='1':
                u = Student.objects.filter(~Q(status="deleted")).order_by('sname')          # sort by name
            elif f=='2':
                u = Student.objects.filter(~Q(status="deleted")).order_by('semail')         # sort by email
            elif f=='3':
                u = Student.objects.filter(~Q(status="deleted")).order_by('-date')          # sort by date

            elif f:                                                                         # search
                if len(f)>20:
                    u = Student.objects.none()
                else:
                    allStudentName= Student.objects.filter(sname__icontains=f).filter(~Q(status="deleted"))
                    allStudentEmail= Student.objects.filter(semail__icontains=f).filter(~Q(status="deleted"))
                    u = allStudentName.union(allStudentEmail)
                if u.count()==0:
                    messages.warning(request, "No search results found. Please refine your query.")
                    
                    return redirect('showusers')

            elif request.GET.getlist('selectedCourseFilter'):                               # Coursewise filter

                filterlist = request.GET.getlist('selectedCourseFilter')

                if "Deleted" in filterlist:
                    u = Student.objects.filter(status="deleted")
                    filterlist.remove("Deleted")
                else:
                    u = Student.objects.all()
                
                for i in filterlist:
                    co = Course.objects.get(id=i)
                    temp = Student.objects.filter(course=co)
                    u = u & temp
            elif request.GET.getlist('selectedBatchFilter'):                               # Batchwise filter

                filterlist = request.GET.getlist('selectedBatchFilter')

                if "Deleted" in filterlist:
                    u = Student.objects.filter(status="deleted")
                    filterlist.remove("Deleted")
                else:
                    u = Student.objects.all()
                
                for i in filterlist:
                    b = Batch.objects.get(id=i)
                    temp = Student.objects.filter(batch=b)
                    u = u & temp
            else:
                u = Student.objects.filter(~Q(status="deleted"))
            
            d = {}
            l1=[]
            l2=[]
            for i in u:
                a = Student.objects.get(id=i.id)
                l1.append(a.course.all())
                l2.append(a.batch.all())
            
            en = request.GET.get('entry')
            if en:
                request.session['entry']= int(en)
            
            student_paginator = Paginator(u, request.session['entry'])
            page_num = request.GET.get('page')
            student_page = student_paginator.get_page(page_num)

            course_paginator = Paginator(l1,request.session['entry'])
            course_page = course_paginator.get_page(page_num)

            batch_paginator = Paginator(l2,request.session['entry'])
            batch_page = batch_paginator.get_page(page_num)
            
            us = zip(student_page,course_page,batch_page)

            d["admin"]=user
            d["users"]=us
            d['user']=student_page
            d["courses"]=c
            d["batches"]=bat
            d["enteries"]=request.session['entry']
            
            return render(request, 'adminmodule/showusers.html', d)
        else:

            return redirect('../adminmodule/login')
    except:
        return redirect('../adminmodule/login')

def activateuser(request):
    try:
        if request.session['userid'] !="":
            b = request.GET['data']
            ins = Student.objects.get(pk=b)
            flag=0
            if ins.status=="Active":
                ins.status="Inactive"
                ins.save()

                mess= f'Hello, {ins.sname} \n your account has been successfully  DEACTIVATED \n Now you cannot  access the courses \n Thanks.'
                send_mail(
                "Welcome to Educap ",
                mess, 
                settings.EMAIL_HOST_USER,
                [ins.semail],
                fail_silently = False

                )
                flag=1
            if ins.status=="Inactive" and flag==0:
                ins.status="Active"
                ins.save()

                mess= f'Hello, {ins.sname} \n your account has been successfully ACTIVATED \n Now you can access the courses \n Thanks.'
                send_mail(
                "Welcome to Educap ",
                mess, 
                settings.EMAIL_HOST_USER,
                [ins.semail],
                fail_silently = False

                )
              
            return redirect('../adminmodule/showusers')
        else:
            return redirect('../adminmodule/login')
    except:
        return redirect('../adminmodule/login')
    # try:
    #     if request.session['userid'] !="":
    #         b = request.GET['data']
    #         inactivebranch = Student.objects.get(pk=b)
    #         flag=0
    #         if inactivebranch.status=="Active":
    #             inactivebranch.status="Inactive"
    #             flag=1
    #         if inactivebranch.status=="Inactive" and flag==0:
    #             inactivebranch.status="Active"
    #         inactivebranch.save()
    #         return redirect('../adminmodule/showusers')
    #     else:
    #         return redirect('../adminmodule/login')
    # except:
    #     return redirect('../adminmodule/login')

def userCourseUpdate(request):
    try:
        if request.session['userid'] !="":
            
            stu = Student.objects.get(id=request.GET["sid"])

            # Remove student from batch which got unselected
            cr = stu.course.all()
            for i in cr:
                if i.id not in request.GET.getlist('selectedCourse'):
                    br = Batch.objects.filter(cid=i)
                    for j in br:
                        stu.batch.remove(j)

            # removed all Courses from student
            for i in Course.objects.all():
                try:
                    stu.course.remove(i)
                except:
                    pass
            
            # Add all selected Courses
            l = request.GET.getlist('selectedCourse')
            for i in l:
                c= Course.objects.get(id=i)
                stu.course.add(c)
            

            return redirect('../adminmodule/showusers')
        else:
            return redirect('../adminmodule/login')
    except:
        return redirect('../adminmodule/login')

def userBatchUpdate(request):
    try:
        if request.session['userid'] !="":
            
            stu = Student.objects.get(id=request.GET["sid"])
            
            for i in Batch.objects.all():
                try:
                    stu.batch.remove(i)
                except:
                    pass
            # removed all Batches from student


            l = request.GET.getlist('selectedBatch')
            for i in l:
                b= Batch.objects.get(id=i)
                stu.batch.add(b)
            # all selected Batches

            return redirect('../adminmodule/showusers')
        else:
            return redirect('../adminmodule/login')
    except:
        return redirect('../adminmodule/login')
