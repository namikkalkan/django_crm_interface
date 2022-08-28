from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decoraters import *



@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()

    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            messages.success(request, 'Succesfully created ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unauthenticated_user
def loginPage(request):


    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'accounts/login.html', context)

def userPage(request):
    context={}
    return render (request,'accounts/user.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    orders_reversed = orders[::-1]
    customers = Customer.objects.all()
    total_customer = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    context = {'orders': orders, 'orders_reversed': orders_reversed, 'customers': customers,
               'total_customer': total_customer, 'total_orders': total_orders,
               'delivered': delivered, 'pending': pending}
    return render(request, 'accounts/dashboard.html', {'context': context})


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_order = orders.count()

    mfilter = OrderFilter(request.GET, queryset=orders)
    orders = mfilter.qs

    context = {'customer': customer, 'orders': orders,
               'total_order': total_order, 'mfilter': mfilter}

    return render(request, 'accounts/customer.html', {'context': context})

@login_required(login_url='login')
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form,'customer':customer}
    return render(request, 'accounts/update_customer.html', context)


@login_required(login_url='login')
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=5)
    customer = Customer.objects.get(id=pk)
    customer_name = customer.name
    # form = OrderForm(initial={'customer':customer})
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        # print('Printing POST:', request.POST)
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset': formset, 'customer': customer, 'customer_name': customer_name}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form, "item": order, "order_c": order.customer}
    return render(request, 'accounts/update_form.html', context)


@login_required(login_url='login')
def deleteOrder(request, ppk):
    order = Order.objects.get(id=ppk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {"item": order, "order_c": order.customer}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['admin'])
def deleteCustomer(request, ppk):
    customer = Customer.objects.get(id=ppk)

    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {"customer": customer}
    return render(request, 'accounts/customer_delete.html', context)

@login_required(login_url='login')
def createCustomer(request):
    form = CustomerForm()

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/create_customer.html', context)
