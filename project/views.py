from email.message import EmailMessage
from django.core.mail import send_mail
from uuid import uuid4
from django.http import HttpResponse,HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib import messages
import razorpay
from Ecommerce import settings
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

def register(request): 
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_token=str(uuid4())
            customer = Customer.objects.create(
                user=user,
                name=user.first_name,
                email=user.email,
                auth_token=auth_token
            )
            order=Order.objects.create(
                customer=customer,
                order_type='cart_order'
            )
            customer.save()
            order.save()
            send_email(user.email,auth_token)
            return render(request,'token.html')
    context = {
        'form': form
    }
    return render(request, 'register.html', context)

def send_email(email , token):
    subject = 'Your accounts need to be verified'
    message = f'Hi click the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message , email_from ,recipient_list )


def verify(request,auth_token):
    try:
        customer=Customer.objects.filter(auth_token=auth_token).first()
        if customer:
            if customer.is_verified:
                messages.success(request, 'Your account is already verified.')
                return render(request,'register_success.html')
            else:
                customer.is_verified=True
                customer.save()
                messages.success(request, 'Your account is successfully verified.')
                return render(request,'register_success.html')
        else:
            return HttpResponse('Error')
    except:
        return HttpResponse('Error')

def loginn(request):
    if request.method == 'POST':
        name = request.POST['username']
        password = request.POST['password']

        user_obj = User.objects.filter(username = name).first()
        customer_obj = Customer.objects.filter(user = user_obj ).first()

        if not customer_obj.is_verified:
            messages.info(request, 'Profile is not verified check your mail.')
            send_email(user_obj.email,customer_obj.auth_token)
            return redirect('login')


        user = authenticate(request, username=name, password=password)
        if user is not None:
            login(request, user)
            return redirect("category")

        else:
            messages.info(
                request, "Invalid credintials, please check username and password.")
            return redirect("login")
    else:
        return render(request, 'login.html')

def logoutt(request):
    logout(request)
    return redirect("category")

def profile(request):
    customer=request.user.customer
    return render(request,'profile.html', {'customer':customer})

def update_profile(request):     
    customer=request.user.customer
    form=UpdateProfileForm(request.POST, instance=customer)
    if form.is_valid():
        form.save()
        return redirect('category')
    else:
        return render(request,'profile.html',{'customer':customer})

def store(request, id):
    if 'q' in request.GET:
        q = request.GET['q']
        category = Category.objects.get(id=id)
        s=(Q(name__icontains=q) | Q(price__icontains=q))
        product = Product.objects.filter(s,category=category)

    else:
        category = Category.objects.get(id=id)
        product = Product.objects.filter(category=category)
    context = {'product': product, 'category': category}
    return render(request, 'store.html', context)


def destroy(request, id):
    order = OrderItem.objects.get(id=id)
    order.delete()
    return redirect("cart")

def category(request):
    if 'q' in request.GET:
        q = request.GET['q']
        category = Category.objects.filter(name__icontains=q)
    else:
        category = Category.objects.all()
        
    context = {
        'category': category
    }
    return render(request, 'category.html', context)

def increase_item_quantity(request, id):
    order_item = OrderItem.objects.get(id=id)
    order_item.quantity += 1
    order_item.save()
    return redirect('cart')

def decrease_item_quantity(request, id):
    order_item = OrderItem.objects.get(id=id)
    if order_item.quantity == 1:
        return redirect('cart')
    else:
        order_item.quantity -= 1
        order_item.save()
        return redirect('cart')

def increase_quantity(request, id):
    product=Product.objects.get(id=id)
    order_item = OrderItem.objects.get(
        customer=request.user.customer,
        product=product,
        order__ordered=False,
        order__order_type='product_order')
    order_item.quantity += 1
    order_item.save()
    return redirect('view',id=id)

def decrease_quantity(request, id):
    product=Product.objects.get(id=id)
    order_item = OrderItem.objects.get(
        customer=request.user.customer,
        product=product,
        order__ordered=False,
        order__order_type='product_order'
        )
    if order_item.quantity == 1:
        return redirect('view',id=id)
    else:
        order_item.quantity -= 1
        order_item.save()
        return redirect('view',id=id)

@login_required(login_url='login')
def cart(request):
    
    order,created = Order.objects.get_or_create(
        customer=request.user.customer, ordered=False,order_type='cart_order')
        
    items = order.orderitem_set.all()
    get_cart_items_total = sum(
                [item.quantity for item in items]
                )
    get_cart_total_cost = sum(
        [item.product.price*item.quantity for item in items]
        )
    

    context = {
        'order': order,
        'items':items,
        'get_cart_items_total': get_cart_items_total,
        'get_cart_total_cost': get_cart_total_cost,

    }
    return render(request, 'cart.html', context)

@login_required(login_url='login')
def view_order(request):
    try:
        order_items=OrderItem.objects.filter(
            customer=request.user.customer,
            order__ordered=True)
        context={
            'order_items':order_items,
            
        }
        return render(request,'view_orders.html',context)
    except: 
        return HttpResponse('No Orders found')


@login_required(login_url='login')
def cancelled(request):
    try:
       
        cancelled=CancelOrder.objects.filter(customer=request.user.customer)
        context={
        'cancelled':cancelled
        }

        return render(request,'cancelled_order.html',context)
    except:
       return HttpResponse('No cancelled items Found')

@login_required(login_url='login')
def order_status(request,id):
    order_item=OrderItem.objects.get(id=id)
    order=order_item.order
    
    context={
        'order_item':order_item,
        'order':order
    }
    return render(request,'order_status.html',context)

@login_required(login_url='login')
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    order, created = Order.objects.get_or_create(
        customer=request.user.customer,
        ordered=False,
        order_type='cart_order')
    order_item_qs = OrderItem.objects.filter(
        customer=request.user.customer,
        product=product,
        order=order)
    if order_item_qs.exists():
        order_item = OrderItem.objects.get(order=order, product__id=product.id)
        order_item.quantity += 1
        order_item.save()
    else:
        order_item = OrderItem.objects.create(
            customer=request.user.customer,
            product=product,
            order=order,
            quantity=1
        )
        order_item.save()

    return redirect('cart')


def view_item(request,id):
    product=Product.objects.get(id=id)
    customer = request.user.customer
    order,created=Order.objects.get_or_create(customer=customer,product=product,ordered=False,order_type='product_order')
    order_item,created=OrderItem.objects.get_or_create(customer=customer,product=product,order=order)
    total=product.price*order_item.quantity
    context={
        'order_item':order_item,
        'total_cost':total,
        'product':product
    }
    return render(request,'view.html',context)


razorpay_id=settings.razorpay_id
razorpay_account_id=settings.razorpay_account_id
client = razorpay.Client(auth=(razorpay_id, razorpay_account_id))
@login_required(login_url='login')
def buynow(request,id):
    customer = request.user.customer
    product=Product.objects.get(id=id)
    order,created=Order.objects.get_or_create(customer=customer,product=product,ordered=False,order_type='product_order')
    order_item,created=OrderItem.objects.get_or_create(customer=customer,product=product,order=order)
    
    amount=order_item.quantity*product.price 

    DATA = {
        "amount": amount*100,
        "currency": "INR",
        "payment_capture":'0'
    }
    razorpay_order=client.order.create(data=DATA)

    order.transactionId=razorpay_order['id']
    cust_name=customer.name
    cust_phone=customer.mobile
    cust_email=customer.email
    order.customer_address=customer.address
    order.customer_name=customer.name
    order.customer_email=customer.email
    order.customer_mobile=customer.mobile
    order.save()
    callback_url='product_handler'
    
    context={
        'amount': amount,
        'order_id': razorpay_order['id'],
        'orderId':order.id,
        'razorpay_merchant_id':razorpay_id,
        'callback_url':callback_url,
        'order':order,'order_item':order_item,
        'orderId':order.id,
        'product':product,
        'cust_name':cust_name,
        'cust_phone':cust_phone,
        'cust_email':cust_email
    }
    return render(request,'buynow.html',context)

@csrf_exempt 
def product_handler(request):
    customer=request.user.customer
    if request.method=='POST':
        try:
            payment_id=request.POST.get('razorpay_payment_id','')
            order_id=request.POST.get('razorpay_order_id','')
            signature=request.POST.get('razorpay_signature','')
            params_dict={
                'razorpay_payment_id':payment_id,
                'razorpay_order_id':order_id,
                'razorpay_signature':signature
            }

            try:
                order=Order.objects.get(transactionId=order_id)
            except:
                return HttpResponse('505 not found')

            """items=order.orderitem_set.all()
            get_cart_total_cost = sum(
                [item.product.price*item.quantity for item in items]
                )
            amount=get_cart_total_cost*100"""
            result=client.utility.verify_payment_signature(params_dict)
            
            if result is None:
                try:
                    order=Order.objects.get(transactionId=order_id)
                    items=order.orderitem_set.all()
                    get_cart_total_cost = sum(
                        [item.product.price*item.quantity for item in items]
                        )
                    amount=get_cart_total_cost*100
                    client.payment.capture(payment_id,amount)
                    order.ordered=True
                    order.status='pending'
                    order.razorpay_payment_id =  payment_id
                    order.save()
                    template=render_to_string('email1.html', {'name': customer.name,'product':order.product})
                    email=EmailMessage(
                            'Ecom Store',
                            template,
                            settings.EMAIL_HOST_USER,
                            [customer.email],
                        )
                    email.fail_silently=False    
                    email.send()
                    return render(request,'payment_success.html')
                except:
                    return render(request,'payment_failure.html')
            else:
                return render(request,'payment_failure.html')
        except:
            return HttpResponseBadRequest()

@login_required(login_url='login')
def checkout(request):
    
    customer = request.user.customer
    order = Order.objects.get(
        customer=customer,
        ordered=False,
        order_type='cart_order'
    )

    items = order.orderitem_set.all()
    get_cart_items_total = sum(
            [item.quantity for item in items]
            )
    get_cart_total_cost = sum(
        [item.product.price*item.quantity for item in items]
        )
    amount=get_cart_total_cost*100

       
    DATA = {
        "amount": amount,
        "currency": "INR",
        "receipt": str(order.id),
        "payment_capture":'0'
    }
    razorpay_order=client.order.create(data=DATA)
    order.transactionId=razorpay_order['id']
    cust_name=customer.name
    cust_phone=customer.mobile
    cust_email=customer.email
    order.customer_address=customer.address
    order.customer_name=customer.name
    order.customer_email=customer.email
    order.customer_mobile=customer.mobile
    order.save()
        
    callback_url='handle_request'
    context={
        'amount': get_cart_total_cost * 100,
        'order_id': razorpay_order['id'],
        'orderId':order.id,
        'razorpay_merchant_id':razorpay_id,
        'items':items,
        'callback_url':callback_url,
        'order':order,
        'orderId':order.id,
        'get_cart_items_total': get_cart_items_total,
        'get_cart_total_cost': get_cart_total_cost,
        'cust_name':cust_name,
        'cust_phone':cust_phone,
        'cust_email':cust_email
    }
    return render(request,'checkout.html',context)

        
@csrf_exempt 
def handle_request(request):
   
    customer=request.user.customer
    if request.method=='POST':
        try:
            payment_id=request.POST.get('razorpay_payment_id','')
            order_id=request.POST.get('razorpay_order_id','')
            signature=request.POST.get('razorpay_signature','')
            params_dict={
                'razorpay_payment_id':payment_id,
                'razorpay_order_id':order_id,
                'razorpay_signature':signature
            }
            try:
                order=Order.objects.get(transactionId=order_id)
            except:
                return HttpResponse('505 not found')
            
            result=client.utility.verify_payment_signature(params_dict)
            
            if result==None:
                try:
                    order=Order.objects.get(transactionId=order_id)
                    items = order.orderitem_set.all()
                    get_cart_total_cost = sum(
                        [item.product.price*item.quantity for item in items]
                        )
                    amount=get_cart_total_cost*100
                    client.payment.capture(payment_id,amount)
                    order.ordered=True
                    order.status='pending'
                    order.razorpay_payment_id =  payment_id
                    order.save()
                    template=render_to_string('email1.html', {'name': customer.name})
                    email=EmailMessage(
                            'Ecom Store',
                            template,
                            settings.EMAIL_HOST_USER,
                            [customer.email],
                        )
                    email.fail_silently=False    
                    email.send()
                    return render(request,'payment_success.html')
                except:
                    return render(request,'payment_failure.html')
            else:
                return render(request,'payment_failure.html')
        except:
            return HttpResponseBadRequest()

def cancel_order(request,id):
    orderitem=OrderItem.objects.get(id=id)
    cancel=CancelOrder.objects.create(
        customer=request.user.customer,
        order=orderitem.order.id,
        order_item=orderitem.product.name,
        price=orderitem.product.price*orderitem.quantity,
        quantity=orderitem.quantity,
        dateOrdered=orderitem.order.dateOrdered,
        transactionId=orderitem.order.transactionId,
        razorpay_payment_id=orderitem.order.razorpay_payment_id,
        customer_name=orderitem.order.customer_name,
        customer_mobile=orderitem.order.customer_mobile,
        customer_email=orderitem.order.customer_email,
        customer_address=orderitem.order.customer_address
    )
    order=orderitem.order
    
    items=order.orderitem_set.all()
    length=len(items)

    if length>1:
        orderitem.delete()
    else:
        orderitem.delete()
        order.status='cancelled'
        order.save()   
    
    cancel.save()
    return render(request,'cancel.html')
