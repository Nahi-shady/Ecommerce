from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime

from .models import *
from .utils import *

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def store(request):
    Data = cartData(request)
    order = Data['order']
    items = Data['items']
    cartItems = Data['cartItems']


    products = Product.objects.all()
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/store.html', context)


def cart(request):
    Data = cartData(request)
    order = Data['order']
    items = Data['items']
    cartItems = Data['cartItems']
            
    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/cart.html', context)


def checkout(request):
    Data = cartData(request)
    order = Data['order']
    items = Data['items']
    cartItems = Data['cartItems']


    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    action = data['action']
    productId = data['productId']

    customer = request.user.customer
    product = Product.objects.get(id=productId) 
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    
    return JsonResponse('item was added', safe=False)


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                zipcode=data['shipping']['zipcode'],
            )

    else:
        print('user is not logged in!')

    return JsonResponse('payment complete', safe=False)