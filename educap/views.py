from django.shortcuts import HttpResponse,render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from student.models import Student
from adminmodule.models import Course,Assignment,Notes,Video

def home(request):
    courses = Course.objects.all()
    params = {'courses':courses}
    try:
        user1 = Student.objects.get(id=request.session['userid'])

        params["user1"] = user1
        return render(request,"home.html",params)
    except:
        return render(request, "home.html",params)

def studentRegistration(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password=request.POST.get('password')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        username=request.POST.get('username')
        print(email,password,firstname,lastname,username)
        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email already exits")
            return redirect('/')
        else:
            user = User(email=email,password=password,first_name=firstname,last_name=lastname,username=username)
            user.set_password(password)
            user.save()
            messages.success(request, "student profile is created successfully")
            return redirect('/')
    # return render(request,"home.html")
    return redirect("/")

def student_login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "student logged in successfully")
            return render(request,'student/homes.html')
        else:
            messages.warning(request,'Invalid credentials')
            return render(request,"home.html")
    return redirect("/")

def viewcourse(request):
    try:
        user1 = Student.objects.get(id=request.session['userid'])
        data = request.GET['data']
        c = Course.objects.get(pk=data)
        n = Notes.objects.filter(cid=c,status="active")
        a = Assignment.objects.filter(cid=c, status="active")
        v = Video.objects.filter(cid=c, status="active")
        params = {'course': c,"notes":n,"assignments":a,"videos":v,"user1":user1}
        return render(request,"viewcourse.html",params)
    except:
        messages.warning(request,'Login First')
        return redirect('../')