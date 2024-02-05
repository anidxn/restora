from django.db import models

# Create your models here.
class Feedback(models.Model): # ******* django will create a table with name = Modelname+S, so it will become Feedbacks
    # https://docs.djangoproject.com/en/4.2/ref/models/fields/
    
    cname = models.CharField('customer name', max_length=50)  # customer name is the label used for this field in admin panel / form.py
    cemail = models.CharField(max_length=100)
    cphn = models.CharField(max_length=15)
    fbdesc = models.TextField(null=True)
    fbdate = models.DateField()
    fbid = models.AutoField(primary_key=True) # primary keys are read-only fields
    rating = models.IntegerField(default=4) #FloatField(default = 4.0)
    approved = models.BooleanField(default = False)

    # need ..so that in django admin portal the records show some indicating names
    def __str__(self):
        return self.cname
    
class Reservation(models.Model):
    rv_id = models.AutoField(primary_key=True)
    cname = models.CharField('customer name', max_length=50)  # customer name is the label used for this field in admin panel / form.py
    cemail = models.EmailField(max_length=100)
    cphn = models.CharField(max_length=15)
    rv_date = models.DateField()  # *******************
    rv_time = models.TimeField()  # *******************
    ppl_count = models.IntegerField() # ***************
    msg = models.TextField(null=True)
    uid = models.BigIntegerField(default = 0)  # for logged in users ..store uid, so they can check later

    def __str__(self):
        return self.cname


