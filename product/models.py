from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Category(models.TextChoices):
    COMPUTERS = 'Computers'
    FOOD = 'Food'
    KIDS = 'Kids'
    HOME = 'Home'
    
    
class Product(models.Model):
    name = models.CharField(max_length=200, default="",blank=False)
    description = models.TextField(max_length=1000, default="",blank=False)
    price = models.DecimalField(max_digits=7, decimal_places=2,default=0)
    brand = models.CharField(max_length=200,blank=False)
    category = models.CharField(max_length=40,choices=Category.choices)
    ratings = models.DecimalField(max_digits=3,decimal_places=2,default=0)
    stock = models.IntegerField(default=0)
    ceateAt=models.DateTimeField(auto_now_add=True)
    user = models.name = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    
    #return of the object with his name
    def __str__(self):
        return self.name
    
class Review(models.Model):
    product = models.ForeignKey(Product, null=True, on_delete=models.CASCADE,related_name='reviews') #Cascade yaani marboutin b baadhum, ken yétneha wahed fihoum lokher yetfassakh toul!
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) #ken enahou l user yab9a l review
    rating = models.IntegerField(default=0)
    comment = models.TextField(max_length=200)
    ceateAt=models.DateTimeField(auto_now_add=True)    
   
    #return of the object with his name
    def __str__(self):
        return self.comment #yaani yarj3élna 3la type l comment   