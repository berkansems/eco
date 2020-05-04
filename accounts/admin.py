from django.contrib import admin

# Register your models here.


from accounts.models import Customer, Product, Tag, Order

admin.site.register(Customer)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(Order)
