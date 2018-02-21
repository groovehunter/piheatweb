from django.db import models

# default Rule
DEFAULT_RULE = 1
DEFAULT_MOTOR= 1
DEFAULT_TOGGLE_RULE = 2


class Rule(models.Model):

    name = models.CharField(max_length=32)
    descr= models.CharField(max_length=255)
    logic= models.CharField(max_length=255)
    count= models.PositiveIntegerField()


class RuleHistory(models.Model):

    rule_id = models.ForeignKey(Rule, on_delete=models.CASCADE, default=DEFAULT_RULE)
    name = models.CharField(max_length=32)
    descr= models.CharField(max_length=255)
    logic= models.CharField(max_length=255)
    count= models.PositiveIntegerField()




class Motor(models.Model):
    
    name    = models.CharField(max_length=16)
    descr   = models.CharField(max_length=255)
    last_toggle = models.CharField(max_length=16)
    


class Toggle(models.Model):
        
    toggle = models.ForeignKey(Motor, on_delete=models.CASCADE, default=DEFAULT_MOTOR)
    dtime   = models.DateTimeField('date published')
    state   = models.BooleanField('Status')
    rule    = models.ForeignKey(Rule, on_delete=models.CASCADE, default=DEFAULT_TOGGLE_RULE)


