from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings

# Create your views here.
from accounts import rabbitConnection
from accounts.decorators import unauthenticated_user, allowed_users, user_analyser
from accounts.filters import OrderFilter
from accounts.forms import OrderForm, CustomerForm, CreateUserForm
from accounts.models import Order, Customer, Product
from django.forms import inlineformset_factory
import logging

from accounts.rabbitConnection import RabbitConnection

logger=logging.getLogger("logger2")
connection = RabbitConnection()


@login_required(login_url='signin')
#@allowed_users(allowed_roles=['admin'])
@user_analyser
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    totalCustomers = customers.count()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    totalOrdersAmount = 0
    for order in orders:
        totalOrdersAmount += order.adet

    context = {'orders': orders,
               'customers': customers,
               'totalOrders': totalOrders,
               'totalCustomers': totalCustomers,
               'delivered': delivered,
               'pending': pending,
               'totalOrdersAmount':totalOrdersAmount
               }
    return render(request, 'accounts/dashboard.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'accounts/products.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    ordersCount = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,
               'orders': orders,
               'ordersCount': ordersCount,
               'myFilter': myFilter}

    return render(request, 'accounts/customer.html', context)



@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def createOrder(request, pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=4)
    customer = Customer.objects.get(id=pk)
    formSet = orderFormSet(queryset=Order.objects.none(), instance=customer)
    if request.method == 'POST':
        formSet = orderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()

            logger.info("order created by admin")
            return redirect('customer', pk)
    context = {'formSet': formSet}
    return render(request, 'accounts/order_form.html', context)



@login_required(login_url='signin')
@allowed_users(allowed_roles=['customer'])
def newOrderCustomer(request,pk):
    orderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'adet'), extra=4)
    customer = Customer.objects.get(id=pk)
    formSet = orderFormSet(queryset=Order.objects.all(), instance=customer)
    if request.method == "POST":
        formSet = orderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            customer = Customer.objects.get(id=pk)
            orders = customer.order_set.all()

            for order in orders:
                order.totalCost=order.adet * order.product.price
                order.save()

            logger.info("orders created by customer")
        return redirect('payment',pk)


    context={'formSet':formSet}
    return render(request,'accounts/new_customer_order.html',context)



@login_required(login_url='signin')
@allowed_users(allowed_roles=['customer'])
def payment(request,pk):
    customer=Customer.objects.get(id=pk)
    orders=customer.order_set.all()

    totalOrderingCost=0
    for order in orders:
        totalOrderingCost+=order.totalCost

    totalOrdersAmount=0
    for order in orders:
        totalOrdersAmount += order.adet

    context={
        'orders':orders,
        'totalOrderingCost':totalOrderingCost,
        'totalOrdersAmount':totalOrdersAmount
    }
    return render(request,'accounts/payment.html',context)



@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            logger.info("order updated by admin")
            return redirect('customer', order.customer.pk)
    context = {'form': form}
    return render(request, 'accounts/update_order.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()

        logger.info("order deleted by admin")
        return redirect('customer', order.customer.pk)
    context = {'order': order}
    return render(request, 'accounts/delete_order.html', context)

@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    if request.method == 'POST':
        customer.delete()

        logger.info("customer deleted by admin")
        return redirect('home')
    context = {'customer': customer}
    return render(request, 'accounts/delete_customer.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()

            logger.info("customer info changed by admin")
            return redirect('customer', pk)
    context = {'form': form}
    return render(request, 'accounts/update_customer.html', context)


@login_required(login_url='signin')
@allowed_users(allowed_roles=['admin'])
def createCustomer(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            #group = Group.objects.get(name='customer')
            #user.groups.add(group)
            #Customer.objects.create(
            #   user=user,
            #   name=user.username
            #)

            logger.info("customer created by admin")

            return redirect('signout')
    context = {'form': form}
    return render(request, 'accounts/create_customer.html',context)

@unauthenticated_user
def signUp(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            #user = form.save()
            form.save()
            #group = Group.objects.get(name='customer')
            #user.groups.add(group)
            #Customer.objects.create(
            #    user=user,
            #    name=user.username
            #)
            logger.info("customer registered successfully")
            return redirect('signin')
        else:
            logger.error("registeration failed")

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)


@unauthenticated_user
def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            logger.info("customer signin successfully")
            connection.write_to_queue("customer signin successfully",1)
            return redirect("home")
        else:
            logger.error("Username or Password is incorrect")
            connection.write_to_queue("Username or Password is incorrect",2)
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'accounts/signin.html', context)


def signOut(request):
    logout(request)
    logger.info("user or admin logout")
    return redirect('signin')


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='signin')
def userPage(request):

    orders = request.user.customer.order_set.all()
    totalOrders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    totalOrdersAmount = 0
    for order in orders:
        totalOrdersAmount += order.adet

    context = {'orders': orders,
               'totalOrders': totalOrders,
               'delivered': delivered,
               'pending': pending,
               'totalOrdersAmount':totalOrdersAmount
               }
    return render(request, 'accounts/user.html', context)


def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            logger.info("settings of account changed")

    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


def email(request):

    return render(request,'accounts/reset_password_sent.html')