from datetime import datetime
from django.db import models
from django.forms import DateField
# from student.models import Student

class Admins(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50,default='12345')
    status = models.CharField(max_length=10,default="active")

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=50)
    desc = models.CharField(max_length=100)
    img = models.ImageField(upload_to="images/",default="")
    status = models.CharField(max_length=10, default="active")

    def __str__(self):
        return self.name

class Notes(models.Model):
    cid = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default="abc")
    file = models.FileField(upload_to="notes/", default='')
    status = models.CharField(max_length=10, default="active")

class Assignment(models.Model):
    cid = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default="abc")
    file = models.FileField(upload_to="assignments/", default='')
    status = models.CharField(max_length=10, default="active")

class Video(models.Model):
    cid = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default="abc")
    file = models.FileField(upload_to="videos/", default='')
    status = models.CharField(max_length=10, default="active")

class Batch(models.Model):
    cid = models.ForeignKey(Course,on_delete=models.CASCADE)
    days = models.CharField(max_length=100,default=" ")
    date= models.CharField(max_length=100,default=" ")
    time= models.CharField(max_length=100,default=" ")
    a=models.CharField(max_length=50,default="Pm")
    status = models.CharField(max_length=10, default="active")
    def __str__(self):
        return self.days

class Batch_videos(models.Model):
    bid = models.ForeignKey(Batch,on_delete=models.CASCADE)
    name = models.CharField(max_length=50,default="abc")
    file = models.FileField(upload_to="batch_videos/", default='')
    status = models.CharField(max_length=10, default="active")
    # def __str__(self):
    #     return self.file
   