from django.db import models



class Motor(models.Model):
    
    name    = models.CharField(max_length=16)
    descr   = models.CharField(max_length=255)
    last_toggle = models.CharField(max_length=16)
    


class Toggle(models.Model):
        
    toggle = models.ForeignKey(Motor, on_delete=models.CASCADE)
    dtime   = models.DateTimeField('date published')
    state   = models.BooleanField('Status')