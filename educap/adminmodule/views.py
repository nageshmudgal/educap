from django.shortcuts import render,redirect
from .models import Admins


def home(request):
    try:
        if request.session['userid'] != "":
            admin = Admins.objects.get(id=request.session['userid'])

            params = {"admin": admin}
            return render(request, "admin/homes.html", params)
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

    return render(request,'admin/login.html')

def logout(request):
    try:
        del request.session['userid']
        return redirect('../')
    except:
        return redirect("../adminmodule/login")

