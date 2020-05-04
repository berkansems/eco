from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=20, null=True)

    email = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    profilePicture = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    Category = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor'),
        ('Electronic', 'Electronic')
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=Category)
    description = models.CharField(max_length=200, null=True)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name


class Order(models.Model):
    Status = (
        ('Pending', 'Pending'),
        ('Out of Delivery', 'Out Of Delivery'),
        ('Delivered', 'Delivered')
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    dateCreated = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=Status, default='Pending')
    note = models.CharField(max_length=1000, null=True)
    adet = models.IntegerField(null=True)
    totalCost= models.IntegerField(null=True)

    def __str__(self):
        return self.customer.name + " : " + self.product.name
