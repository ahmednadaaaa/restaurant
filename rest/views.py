from datetime import timezone
from .decorators import notLoggedUsers , allowedUsers, forAdmins
from django.forms import inlineformset_factory

from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from .forms import OrderForm,CreateNewUser,CustomerForm
from django.contrib.auth import authenticate ,login  , logout
from django.contrib.auth.decorators import  login_required
import requests
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from .models import *
# Create your views here.


def menu(request):
    meals_list = Meal.objects.all()
    context = {'meals_list': meals_list}
    return render(request, 'menu.html', context)


def index(request):
    meals_list = Meal.objects.all()
    context = {'meals_list': meals_list}

    if request.method == 'POST' and 'btnbooking' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        date_reservation = request.POST.get('date_reservation')
        num_people = request.POST.get('num_people')
        message = request.POST.get('message')

        if name and email and date_reservation and num_people and message:
            if request.user.is_authenticated and not request.user.is_anonymous:
                book_table = BookTable.objects.create(name=name, email=email, date_reservation=date_reservation, num_people=num_people, message=message)
                context['is_added'] = True
                messages.success(request, 'Your order has been submitted successfully.')
            else:
                messages.error(request, 'You need to be logged in to book a table.')
            messages.error(request, 'Please fill in all the required fields.')

    return render(request, 'index.html', context)


def meal_detail(request, meal_id):
    meal = get_object_or_404(Meal, pk=meal_id)
    related_meals = Meal.objects.filter(category=meal.category).exclude(id=meal.id)
    context = {
        'meal': meal,
        'related_meals': related_meals,
    }
    return render(request, 'meal_detail.html', context)

@login_required(login_url='login')
def booking(request):
    context = {}
    if request.method == 'POST' and 'btnbooking' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        date_reservation = request.POST.get('date_reservation')
        num_people = request.POST.get('num_people')
        message = request.POST.get('message')

        if name and email and date_reservation and num_people and message:
            if request.user.is_authenticated and not request.user.is_anonymous:
                book_table = BookTable.objects.create(name=name, email=email, date_reservation=date_reservation, num_people=num_people, message=message)
                context['is_added'] = True
                messages.success(request, 'Your order has been submitted successfully.')
            else:
                messages.error(request, 'You need to be logged in to book a table.')  # Display error message if user is not authenticated
        else:
            messages.error(request, 'Please fill in all the required fields.')  # Display error message if any field is missing

    return render(request, 'booking.html', context)


def contactus(request):
    context = {}
    if request.method == 'POST' and 'btncontent' in request.POST:
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if name and email and subject and message:
            if request.user.is_authenticated and not request.user.is_anonymous:
                contact = ContactUs.objects.create(name=name, email=email, subject=subject, message=message)
                context['is_added'] = True
                messages.success(request, 'We have received your message. We will get back to you soon.')
            else:
                messages.error(request, 'You need to be logged in to submit the form.')
        else:
            messages.error(request, 'Please fill in all the required fields.')
    return render(request, 'contact.html', context)


def add_to_cart(request):

    if 'pro_id' in request.GET and 'qty' in request.GET and 'price' in request.GET and request.user.is_authenticated and not request.user.is_anonymous :

        pro_id = request.GET['pro_id']
        qty = request.GET['qty']

        order = Order.objects.all().filter(user=request.user, is_finished=False)

        if not Meal.objects.all().filter(id=pro_id).exists():
            return redirect('meal_detail')
        pro = Meal.objects.get(id=pro_id)

        if order:
            messages.success(request,'Success order')
            old_order = Order.objects.get(user=request.user.id, is_finished=False)
            if OrderDetail.objects.all().filter(order=old_order, product=pro).exists():
                orderdetails = OrderDetail.objects.get(order=old_order, product=pro)
                orderdetails.quantity += int(qty)
                orderdetails.save()
            else :
                orderdetails = OrderDetail.objects.create(product=pro,
                order=old_order, price=pro.price, quantity=qty)
            messages.success(request, 'was added to cart for old order')
        else :
            messages.success(request,'هنا سوف يتم عمل طلب')
            new_order = Order()
            new_order.user =request.user
            new_order.order_date = timezone.now()
            new_order.is_finished = False
            new_order.save()
            oderdetails = OrderDetail.objects.create(product=pro, order=new_order, price=pro.price, quantity=qty)
            messages.success(request, 'was added to cart for new order')

        return redirect('/meal/' + request.GET['pro_id'])

    else:

      return redirect('index')


def cart(request):
    context = None
    if Order.objects.all().filter(user=request.user.id, is_finished=False):
        order = Order.objects.get(user=request.user.id, is_finished=False)
        orderdetails = OrderDetail.objects.all().filter(order=order)
        total = 0
        for sub in orderdetails:
            total +=sub.price * sub.quantity

        context = {
            'order':order,
            'orderdetails':orderdetails,
            'total':total,

        }

    return render(request, 'cart.html', context)


def remove_from_cart(request, orderdetails_id):
   if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
    orderdetails = OrderDetail.objects.get(id=orderdetails_id)
    if orderdetails.order.user.id==request.user.id:
     orderdetails.delete()
    return redirect('cart')


def add_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetail.objects.get(id=orderdetails_id)
        orderdetails.quantity +=1
        orderdetails.save()

    return redirect('cart')


def sub_qty(request, orderdetails_id):
    if request.user.is_authenticated and not request.user.is_anonymous and orderdetails_id:
        orderdetails = OrderDetail.objects.get(id=orderdetails_id)
        if orderdetails.quantity > 1:
            orderdetails.quantity -= 1
            orderdetails.save()

    return redirect('cart')


def show_orders(request):
    context = None
    all_orders = None
    if request.user.is_authenticated and not request.user.is_anonymous:
        all_orders = Order.objects.all().filter(user=request.user)
        if all_orders:
            for x in all_orders:
                order = Order.objects.get(id=x.id)
                orderdetails = OrderDetail.objects.all().filter(order=order)
                total = 0
                for sub in orderdetails:
                    total +=sub.price * sub.quantity
                    x.total = total
                    x.items_count = orderdetails.count
    context = {'all_orders':all_orders}
    return render(request, 'show_orders.html', context)
@notLoggedUsers
def register(request):
    form = CreateNewUser()
    if request.method == 'POST':
        form = CreateNewUser(request.POST)
        if form.is_valid():
            user = form.save()  
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')  

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)  
                messages.success(request, f'{username} Created and Logged in Successfully!')
                return redirect('index')

    context = {'form': form}
    return render(request, 'register.html', context)
def userLogin(request):

        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Credentials error')

        context = {}

        return render(request, 'login.html', context)


def userLogout(request):
    logout(request)
    return redirect('login')


def admin(request):

    return render(request, 'dashboard/index.html')


def emp(request):
    employe = Employe.objects.all()
    context = {
               'employe': employe
               }
    return render(request, 'dashboard/employe.html',  context)


def users(request):
    users = User.objects.all()
    context = {
               'users': users
               }
    return render(request, 'dashboard/users.html',  context)


def table(request):
    booktable = BookTable.objects.all()
    context = {
               'booktable': booktable
               }
    return render(request, 'dashboard/table.html',  context)


def message(request):
    contactus = ContactUs.objects.all()
    context = {
               'contactus': contactus
               }
    return render(request, 'dashboard/message.html',  context)


def ordered(request):
    orders = Order.objects.all()
    context = {
               'orders': orders
               }
    return render(request, 'dashboard/order.html',  context)


def meals(request):
    meals = Meal.objects.all()
    context = {
               'meals': meals
               }
    return render(request, 'dashboard/meals.html',  context)


def payment(request):
    if request.method == 'POST' and 'btnpayment' in request.POST:
        ship_address = request.POST.get('ship_address')
        ship_phone = request.POST.get('ship_phone')
        payment_method = request.POST.get('payment_method')
        order = None
        is_added = False

        if request.user.is_authenticated and not request.user.is_anonymous:
            if Order.objects.filter(user=request.user.id, is_finished=False).exists():
                order = Order.objects.get(user=request.user.id, is_finished=False)
                order_details = OrderDetail.objects.filter(order=order)
                total = sum(detail.price * detail.quantity for detail in order_details)

                if payment_method == 'card':
                    card_number = request.POST.get('card_number')
                    expire = request.POST.get('expire')
                    security_code = request.POST.get('security_code')
                    payment = Payment.objects.create(order=order, shipment_address=ship_address,
                                                     shipment_phone=ship_phone, card_number=card_number,
                                                     expire=expire, security_code=security_code)
                    is_added = True
                elif payment_method == 'cash':
                    if Order.objects.filter(user=request.user.id, is_finished=False).exists():
                        order = Order.objects.get(user=request.user.id, is_finished=False)
                        order_details = OrderDetail.objects.filter(order=order)
                        total = sum(detail.price * detail.quantity for detail in order_details)

                    cash_payment = CashPayment.objects.create(order=order,
                                                              shipment_address=ship_address,
                                                              shipment_phone=ship_phone)
                    is_added = True

                order.is_finished = True
                order.save()
                messages.success(request, 'Your order is finished')

        context = {
            'ship_address': ship_address,
            'ship_phone': ship_phone,
            'is_added': is_added,
        }
    else:
        # Fetch and display order details
        order = None
        if request.user.is_authenticated and not request.user.is_anonymous:
            order = Order.objects.filter(user=request.user.id, is_finished=False).first()
        context = {'order': order}


    return render(request, 'payment.html', context)
def serv(request):
    pass
    return render(request, 'service.html')

from rest_framework import generics
from .models import Meal, Customer, Employe, Order, OrderDetail, BookTable, ContactUs, Payment, CashPayment
from .serializers import (
    MealSerializer, CustomerSerializer, EmployeSerializer, 
    OrderSerializer, OrderDetailSerializer, BookTableSerializer, 
    ContactUsSerializer, PaymentSerializer, CashPaymentSerializer
)

class MealListCreateView(generics.ListCreateAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

class MealDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
