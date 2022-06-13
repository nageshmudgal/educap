from django.shortcuts import HttpResponse,render,redirect
from django.contrib.auth.models import User
from django.contrib import messages
from student.models import Student

def home(request):
    try:
        user1 = Student.objects.get(id=request.session['userid'])

        params = {"user1": user1}
        print("yes")
        return render(request,"home.html",params)
    except:
        return render(request, "home.html")

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