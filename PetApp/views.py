from django.shortcuts import render, redirect, HttpResponse
from PetApp.models import Pet, Cart, Orders
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q
import razorpay
import random
from django.core.mail import send_mail


# gmail integration app password (PetStore) - luns efdy vrgb yajx

# Create your views here.
def homeFunction(request):
    context = {}
    data = Pet.objects.all()
    context['pets'] = data
    return render(request,"index.html",context)

def searchPetsByType(request,val):
    context = {}
    data = Pet.objects.filter(type=val)
    context['pets'] = data
    return render(request,"index.html",context)

def sortPetsByPrice(request,dir):
    col=""
    if dir=='asc':
        col='price'
    else:
        col='-price'
    context = {}
    data = Pet.objects.all().order_by(col)
    context['pets'] = data
    return render(request,"index.html",context)

def priceRange(request):
    context = {}
    min = request.GET['min']
    max = request.GET['max']
    c1 = Q(price__lte = max)
    c2 = Q(price__gte = min)
    data = Pet.objects.filter(c1 & c2)
    context['pets']= data
    messages.error(request,'')
    return render(request,'index.html',context)

def petDetails(request,pid):
    context = {}
    data = Pet.objects.filter(id=pid)
    context['pet'] = data[0]
    return render(request,"petdetails.html",context)

def aboutusFunction(request):
    return render(request, 'aboutus.html')

def contactFunction(request):
    return render(request, 'contact.html')

def userlogin(request):
    if request.method=="GET":
        return render(request,"login.html")
    else:
        context = {}
        n = request.POST['username']
        p = request.POST['password']
        if  n=='' or p=='':
            context['error']= 'Please provide all the details.'
            return render(request, 'login.html', context)
        else:
            user = authenticate(username=n, password=p)
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged-in Successfully!')
                return redirect('/')
            else:
                context['error']= 'Invalid User Details!'
                return render(request, 'login.html', context)

def userlogout(request):
    logout(request)
    messages.success(request, 'Logged-out Successfully!')
    return redirect('/')

def register(request):
    if request.method=="GET":
        return render(request,"register.html")
    else:
        # 1) fetch form data
        context = {}
        n = request.POST['username']
        e = request.POST['email']
        p = request.POST['password']
        cp = request.POST['confirm_password']
        # 2) insert data into DB
        if n=='' or e=='' or p=='' or cp=='':
            context['error']= 'Please provide all the details.'
            return render(request, 'register.html', context)
        elif p!=cp:
            context['error']= 'Password does not match!'
            return render(request, 'register.html', context)
        else:
            context['success']= 'Registered Successfully!'
            # user = User.objects.create(username=n, email=e, password=p)
            # for password authentication
            user = User.objects.create(username=n, email=e)
            user.set_password(p)
            user.save()
            return render(request,'login.html', context)
        
def addToCart(request,petid):
    # fetch userid
    userid = request.user.id
    # data will be added to cart only if the userid is known (i.e., for logged in user only)
    if userid is None:
        messages.error(request, 'Please login before adding any item to cart.')
        return render(request,'login.html')
    else:
        users = User.objects.filter(id=userid)
        pets = Pet.objects.filter(id=petid)
        cart = Cart.objects.create(pid=pets[0], uid=users[0])
        cart.save()
        messages.success(request, 'Pet added to cart successfully!')
        return redirect('/')
    
def showMyCart(request):
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)
    context['mycart']= data
    count = len(data)
    total = 0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count']= count
    context['total']= total   
    return render(request,'mycart.html',context)

def removeFromCart(request,cartid):
    data = Cart.objects.filter(id=cartid)
    data.delete()
    messages.success(request, 'Pet removed from cart successfully!')
    return redirect('/mycart')

def confirmOrder(request):
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)
    context['mycart']= data
    count = len(data)
    total = 0
    for cart in data:
        total += cart.pid.price * cart.quantity
    context['count']= count
    context['total']= total   
    return render(request,'confirmorder.html',context)

def makePayment(request):
    '''
    -- fetch current userid
    -- calculate bill amount 
          1. fetch cart details
          2. find bill using loop
    -- using razorpay make payment
    '''
    context = {}
    userid = request.user.id
    data = Cart.objects.filter(uid=userid)
    total = 0
    for cart in data:
        total += cart.pid.price * cart.quantity
    client = razorpay.Client(auth=("rzp_test_9zB92T3BhDnV3l", "bo0RCp9AcGtMxoqpOh9JdUgs"))
    data = { "amount": total*100, "currency": "INR", "receipt": "" }
    payment = client.order.create(data=data)
    context['data']= payment
    return render(request,'pay.html',context)

def placeorder(request):
    #1) fetch cart data
    #userid
    userid = request.user.id
    user = User.objects.filter(id=userid)
    mycart = Cart.objects.filter(uid=userid)
    #orderid
    ordid = random.randrange(10000,99999)
    #2) fetch each cart item insert into orders table
    for cart in mycart:
        #petid and quantity
        pet = Pet.objects.filter(id=cart.pid.id)
        ord = Orders.objects.create(orderid=ordid, uid=user[0], pid=pet[0], quantity=cart.quantity)
        ord.save()
    #3) empty cart data after placing the order
    mycart.delete()
    #4) send order confirmation mail to user
    msgBody = 'Congratulations, your order has been placed successfully! \n' 'Order ID: '+str(ordid)
    custEmail = request.user.email  
    send_mail(
        "PetStore : Order Confirmation",     #subject
        msgBody,                             #body
        "hemisha.d.g@gmail.com",             #sender
        [custEmail],                         #receiver
        fail_silently=False,
    )
    messages.success(request,'Order placed successfully!')
    return redirect('/')

    