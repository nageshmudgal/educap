from django.shortcuts import HttpResponse,render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from student.models import Student
from adminmodule.models import Course,Assignment,Notes,Video,Batch,Batch_videos
from django.db.models import Q
import json
from django.core import serializers
from django.forms.models import model_to_dict
from django.db.models.fields.files import ImageFieldFile

# def encode_datetime(obj):
#     """
#     Extended encoder function that helps to serialize dates and images
#     """
#     if isinstance(obj, datetime.date):
#         try:
#             return obj.strftime('%Y-%m-%d')
#         except:
#             return ''

#     if isinstance(obj, ImageFieldFile):
#         try:
#             return obj.path
#         except:
#             return ''

#     raise TypeError(repr(obj) + " is not JSON serializable")


def home(request):
    try:
        courses = Course.objects.filter(~Q(status="deleted")).filter(name__icontains=request.GET.get('searchquery'))
    except: 
        courses = Course.objects.filter(status='active')
        # courses_js = json.dumps(list[Course.objects.values()])
        # serialized_obj = serializers.serialize('json', [ courses ])
        # assuming obj is your model instance
        # obj = Course.objects.filter(status='active').first()
        # dict_obj = model_to_dict( obj2 )
        # serialized = json.dumps(dict_obj)
    params = {'courses':courses}

    try:
        user = Student.objects.get(id=request.session['studentuser'])

        params["studentuser"] = user
        return render(request,"home.html",params)
    except:
        return render(request, "home.html",params)

def syllabus(request):
    data = request.GET['data']
    c = Course.objects.get(pk=data)
    n = Notes.objects.filter(cid=c,status="active")

    try: 
        studentuser = Student.objects.get(id=request.session['studentuser'])
        params={'notes':n,'course':c,"studentuser":studentuser}
        return render(request,'syllabus.html',params)
    except:
        params={'notes':n,'course':c}
        return render(request,'syllabus.html',params)


def viewcourse(request):
    try:
        user1 = Student.objects.get(id=request.session['studentuser'])
        coid = request.GET['coid']
        t = request.GET['type']
        c = Course.objects.get(pk=coid)
        if c in user1.course.all():

            
            n = Notes.objects.filter(cid=c,status="active").order_by('name')
            
            a = Assignment.objects.filter(cid=c, status="active").order_by('name')
            
            v = Video.objects.filter(cid=c, status="active").order_by('name')
            
            courseBatches = Batch.objects.filter(cid=c)
            batvid = Batch_videos.objects.none()
            for i in courseBatches:
                stuofbatch = Student.objects.filter(batch=i)     # students to batches of that courses

                if user1 in stuofbatch:
                    b = Batch_videos.objects.filter(bid=i).filter(~Q(status="deleted")).order_by('name')
                    batvid = batvid.union(b)
            # if t=="notes":
                # return render(request,"viewcourse.html",{'course': c,"notes":n,"studentuser":user1})
            # elif t=="assignments":
            #     return render(request,"viewcourse.html",{'course': c,"assignments":a,"studentuser":user1})
            # elif t=="videos":
            #     return render(request,"viewcourse.html",{'course': c,"videos":v,"studentuser":user1})
            # elif t=="batchvideos":
            #     return render(request,"viewcourse.html",{'course': c,"batchvideos":batvid,"studentuser":user1})
            # else:
            #     return
            params = {'course': c,"notes":n,"assignments":a,"videos":v,"batchvideos":batvid,"studentuser":user1}
            return render(request,"viewcourse.html",params)
        else:
            messages.warning(request,'You are not enrolled for this Course')
            return redirect('../')
    except:
        messages.warning(request,'Login First')
        return redirect('../')

def asearch(request):
    try:
        user1 = Student.objects.get(id=request.session['studentuser'])
        course = Course.objects.get(id=request.GET.get('coid'))
        if course in user1.course.all():

            assignments = Assignment.objects.filter(cid=course).filter(~Q(status="deleted")).filter(name__icontains=request.GET.get('searchquery'))
            params = {'assignments':assignments}
            params["studentuser"] = user1
            return render(request, "asearch.html",params)
        else:
            messages.warning(request,'You are not enrolled for this Course')
            return redirect('../')
    except: 
        return redirect('../')

def vsearch(request):
    try:
        user1 = Student.objects.get(id=request.session['studentuser'])
        course = Course.objects.get(id=request.GET.get('coid'))
        if course in user1.course.all():

            videos = Video.objects.filter(cid=course).filter(~Q(status="deleted")).filter(name__icontains=request.GET.get('searchquery'))
            params = {'videos':videos}
            params["studentuser"] = user1
            return render(request, "vsearch.html",params)
        else:
            messages.warning(request,'You are not enrolled for this Course')
            return redirect('../')
    except: 
        return redirect('../')

def vlsearch(request):
    # try:
        user1 = Student.objects.get(id=request.session['studentuser'])
        course = Course.objects.get(id=request.GET.get('coid'))
        print("1")
        if course in user1.course.all():
            courseBatches = Batch.objects.filter(cid=course)
            batvid = Batch_videos.objects.none()
            for i in courseBatches:
                stuofbatch = Student.objects.filter(batch=i)     # students to batches of that courses

                if user1 in stuofbatch:                          # if student is in any batch
                    b = Batch_videos.objects.filter(bid=i)       # then all videos of that batch available for user
                    batvid = batvid.union(b)
            print("3")
            batvid = batvid.filter(name__icontains=request.GET.get('searchquery'))
            params = {'batchvideos':batvid}
            params["studentuser"] = user1
            return render(request, "vlsearch.html",params)
        else:
            messages.warning(request,'You are not enrolled for this Course')
            return redirect('../')
    # except: 
    #     return redirect('../')

def nsearch(request):
    try:
        user1 = Student.objects.get(id=request.session['studentuser'])
        course = Course.objects.get(id=request.GET.get('coid'))
        if course in user1.course.all():
            
            notes = Notes.objects.filter(cid=course).filter(~Q(status="deleted")).filter(name__icontains=request.GET.get('searchquery'))
            params = {'notes':notes}
            params["studentuser"] = user1
            return render(request, "search.html",params)
        else:
            messages.warning(request,'You are not enrolled for this Course')
            return redirect('../')
    except: 
        return redirect('../')