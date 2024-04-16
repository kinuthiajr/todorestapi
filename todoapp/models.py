from django.db import models
from django.contrib.auth.models import User

class Todo(models.Model):
    task = models.CharField(max_length=180)
    timestamp = models.DateTimeField(blank=True,auto_now=False,auto_now_add=True)
    comepleted = models.BooleanField(blank=True,default=False)
    updated = models.DateTimeField(blank=True,auto_now=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=False)

    def __str__(self):
        return self.task