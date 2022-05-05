from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CategoryModel(models.Model):
    name = models.CharField(max_length=100)
    image = image= models.ImageField(upload_to='photo/category/')
    objects = models.Manager()

    def __str__(self):
        return self.name

class ProductModel(models.Model):
    category = models.ForeignKey(CategoryModel,on_delete=models.CASCADE)
    image= models.ImageField(upload_to='photo/')
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return self.name

class CustomerModel(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    mobile = models.IntegerField()
    email = models.EmailField()
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    zipcode = models.IntegerField() 
    state = models.CharField(max_length=200)

    objects = models.Manager()

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product= models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def product_total(self):
        return (self.quantity)*(self.product.price)



step = (('Pending','Pending'),('Accepted','Accepted'),('Packing','Packing'),('Shipping','Shipping'),('Deliverd','Deliverd'))


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    customer = models.ForeignKey(CustomerModel,on_delete=models.CASCADE)
    product = models.ForeignKey(ProductModel,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=step,max_length=200,default='Pending')

    @property
    def product_total(self):
        return (self.quantity)*(self.product.price)