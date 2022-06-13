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