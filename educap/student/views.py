from django.shortcuts import render, redirect
from .models import Student


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




