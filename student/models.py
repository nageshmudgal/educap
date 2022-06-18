from django.db import models

# Create your models here.
class Student(models.Model):

    sname = models.CharField(max_length=50)
    semail = models.CharField(max_length=50)
    smobile= models.IntegerField()
    password = models.CharField(max_length=50,default='12345')
    img = models.ImageField(upload_to="userimage/",default="userimage/userprofile.jpg")
    status = models.CharField(max_length=10,default="active")

    def __str__(self):
        return self.sname