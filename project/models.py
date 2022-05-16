from django.db import models
from django.contrib.auth.models import User

class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=50, null=True)
    mobile=models.IntegerField(default=0)
    email=models.CharField(max_length=50, null=True) 
    address=models.TextField(default=0)
    auth_token=models.CharField(max_length=100, default='a')
    is_verified=models.BooleanField(default=False)

    
    def __str__(self):
        return self.name
    

class Category(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(null=True,blank=True)        

    def __str__(self):
        return self.name
        
    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url

class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.SET_NULL, blank=True,null=True)
    name=models.CharField(max_length=200)
    price=models.IntegerField()
    digital=models.BooleanField(default=True, null=True, blank=True)
    image=models.ImageField(null=True,blank=True)
    
    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url=self.image.url
        except:
            url=''
        return url



class Order(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True,null=True)
    order_type=models.CharField(
        max_length=200,blank=True,
        choices=(
            ('cart_order','cart_order'),
            ('product_order','product_order')
            ),
        default='cart_order'
    )
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True,null=True)
    dateOrdered=models.DateTimeField(auto_now_add=True)
    transactionId=models.CharField(max_length=200,null=True)
    razorpay_payment_id=models.CharField(max_length=100, blank=True)
    customer_name=models.CharField(max_length=50, null=True)
    customer_mobile=models.IntegerField(default=0)
    customer_email=models.CharField(max_length=50, null=True) 
    customer_address=models.TextField(default=0)
    status=models.CharField(
        max_length=200,
        choices=(
            ('pending','pending'),
            ('cancelled','cancelled'),
            ('delivered','delivered')
            ),
        default='cart_order'
    )
    ordered=models.BooleanField(default=False)
    
    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL, blank=True,null=True)
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL, blank=True,null=True)
    quantity=models.IntegerField(default=1)
    dateAdded=models.DateTimeField(auto_now_add=True)
    
    
    def get_total(self):
        total=self.product.price * self.quantity
        return total
   
        
    def __str__(self):
       return f'{self.product.name}, Order number {self.id}'

class CancelOrder(models.Model):
    customer=models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True,null=True)
    order=models.IntegerField(default=0)
    order_item=models.CharField(max_length=200, default='a')
    price=models.IntegerField(default=0)
    quantity=models.IntegerField(default=1)
    dateOrdered=models.DateTimeField(auto_now_add=True)
    transactionId=models.CharField(max_length=200,null=True)
    razorpay_payment_id=models.CharField(max_length=100, blank=True)
    customer_name=models.CharField(max_length=50, null=True)
    customer_mobile=models.IntegerField(default=0)
    customer_email=models.CharField(max_length=50, null=True) 
    customer_address=models.TextField(default=0)

