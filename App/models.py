from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userProfile(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='profile_pic',default='sherlock.jpg')
    phone = models.CharField(max_length=500,blank=True,default ="")

    insurance_company_name = models.CharField(max_length=5000,blank=True,default ="")
    address = models.CharField(max_length=5000,blank=True,default ="")
    

    #for hospital details

    hospital_name = models.CharField(max_length=255,blank=True,default ="")
    hospital_address = models.CharField(max_length=255,blank=True,default ="")
    hospital_phone_number = models.CharField(max_length=255,blank=True,default ="")
    hospital_email = models.EmailField(blank=True,default ="")
    hospital_website = models.URLField(blank=True,default ="")
    
    hospital_no_of_doctors = models.IntegerField(blank=True,default =5)
    hospital_no_of_nurses = models.IntegerField(blank=True,default =5)
    hospital_established_year = models.DateField(blank=True,auto_now_add=True)
    

    #for insurance company details

    insurance_company_name = models.CharField(max_length=255,blank=True,default ="")
    insurance_company_address = models.CharField(max_length=255,blank=True,default ="")
    insurance_company_phone_number = models.CharField(max_length=255,blank=True,default ="")
    insurance_company_email = models.EmailField(blank=True,default ="")
    insurance_company_website = models.URLField(blank=True,default ="")
    insurance_company_established_year = models.DateField(blank=True,auto_now_add=True)
    # rating = models.FloatField()
    # policies = models.ManyToManyField(Policy)

    is_a_hospital = models.BooleanField(default=False)
    is_an_insurance_company = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username + " profile"



class Block(models.Model):
    user = models.CharField(max_length=50000)
    transacion_address = models.CharField(max_length=50000)
    ins = models.ForeignKey(User,on_delete=models.CASCADE,blank=True)
    ipn = models.CharField(max_length=50000)
    claimed = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)
    bill_hash = models.CharField(max_length=500, default='', blank=True)
    requested = models.BooleanField(default=False)
    def __str__(self):
        return "Medical Bill"


class BlockAmount(models.Model):

    transacion_address = models.CharField(max_length=50000)
   
    block = models.ForeignKey(Block,on_delete=models.CASCADE)
    
    def __str__(self):
        return "Medical Bill Amount"
    
class Policy(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    image = models.ImageField(upload_to='policy',default='sherlock.jpg')
    name = models.CharField(max_length=5000,blank=True,default ="")
    description = models.CharField(max_length=50000,blank=True,default ="")
    type = models.CharField(max_length=5000,blank=True,default ="")
    amount = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name + ' policy'
    
class Notification(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    message = models.CharField(max_length=5000,blank=True,default ="")
    date = models.DateTimeField(auto_now_add=True)
    ipn = models.CharField(max_length=5000,blank=True,default ="")
    def __str__(self):
        return self.user.username + ' notification'