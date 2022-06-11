from django.db import models

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
    status = models.CharField(max_length=10, default="active")

    def __str__(self):
        return self.name

class File(models.Model):
    cid = models.ForeignKey(Course,on_delete=models.CASCADE)
    file = models.FileField(upload_to="course_files/", default='')
    status = models.CharField(max_length=10, default="active")

