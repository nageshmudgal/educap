from django.db import models

class Admins(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50,default='12345')
    status = models.CharField(max_length=10,default="active")

    def __str__(self):
        return self.name