from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    #kol user lazem ikoun 3andou field wahda barka
    user = models.OneToOneField(User, related_name='profile',on_delete=models.CASCADE)
    reset_password_token = models.CharField(max_length=50,default="",blank=True)
    reset_password_expire = models.DateTimeField(null=True,blank=True)
    
@receiver(post_save, sender=User)
#**kwargs we use kwargs for django signals : like post_save/pre_save
def save_profile(sender,instance,created, **kwargs): 
    print('instance', instance)
    user = instance 
    
    if created:
        profile = Profile(user = user) #user=user hethy les données li besh ijibha!
        profile.save()
        
        
