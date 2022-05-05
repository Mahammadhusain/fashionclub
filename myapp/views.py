from django.shortcuts import render, redirect
from .models import CategoryModel, ProductModel, Order
from .form import (UserCreateForm, SigninForm, UserProfileChangeForm,CustomerForm,PassChangeForm)
from .models import CustomerModel, Cart
from django.http import HttpResponse
from django.contrib import messages
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.db.models import Q
import razorpay
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def ShopView(request):
    men = ProductModel.objects.filter(category_id=5)
    women = ProductModel.objects.filter(category_id=6)
    kids = ProductModel.objects.filter(category_id=7)
    categories = CategoryModel.objects.all()
    usr = request.user
    cart_count = Cart.objects.filter(user=usr).count()
    context = {'men': men, 'women': women,
               'kids': kids, 'categories': categories,'cart_count':cart_count}
    return render(request, 'shop.html', context)


def Add_Cart(request, id):
    if request.method == 'POST':
        usr = request.user
        product = ProductModel.objects.get(id=id)
        data = Cart(
            user=usr,
            product=product,
        )
        data.save()
        messages.info(request, 'Added')
        return redirect('/showcart/')
    else:
        usr = request.user
        product_data = Cart.objects.filter(user=usr)
    return render(request, 'cart.html', {'product_data': product_data})


def PlusQuantity(request, id):
    usr = request.user
    product_data = Cart.objects.get(user=usr, product=id)
    product_data.quantity += 1
    product_data.save()
    return redirect('/showcart/')


def MinusQuantity(request, id):
    usr = request.user
    product_data = Cart.objects.get(user=usr, product=id)
    product_data.quantity -= 1
    if product_data.quantity == 0:
        product_data.delete()
    else:
        product_data.save()
    return redirect('/showcart/',)


def ShowCart(request):
    usr = request.user
    product_data = Cart.objects.filter(user=usr)
    cart_count = Cart.objects.filter(user=usr).count()
    categories = CategoryModel.objects.all()
    amount = 0
    shipping_amt = 40
    final_amt = 0
    data = Cart.objects.filter(user=usr)
    for i in data:
        prod_amt = ((i.product.price)*(i.quantity))
        amount += prod_amt
        final_amt = amount+shipping_amt
        context = {'product_data': product_data, 'cart_count': cart_count,
                   'prod_amt': prod_amt, 'amount': amount, 'final_amt': final_amt,
                   'shipping_amt': shipping_amt,'categories':categories}

    if not data:
        amount = 0
        shipping_amt = 40
        final_amt = 0
        temp_amt = 0
        context = {'product_data': product_data, 'cart_count': cart_count,
                   'temp_amt': temp_amt, 'amount': amount, 'final_amt': final_amt,
                   'shipping_amt': shipping_amt}
    return render(request, 'cart.html', context)


def removeItem(request, id):
    cart_product = Cart.objects.get(id=id)
    cart_product.delete()
    messages.error(
        request, f'{cart_product.product} - Product Removed From Cart')
    return redirect('/showcart/')


def ProfileView(request):
    if request.method == 'POST':
        form = UserProfileChangeForm(request.POST, instance=request.user)
        usr = request.user
        cart_count = Cart.objects.filter(user=usr).count()
        categories = CategoryModel.objects.all()
        context = {'form': form,'cart_count':cart_count,'categories':categories}
        if form.is_valid():
            form.save()
            messages.success(
                request, f'{request.user} - Your Profile Successfully Updated...!')
            return render(request, 'profile.html', context)
    else:
        form = UserProfileChangeForm(instance=request.user)
        usr = request.user
        cart_count = Cart.objects.filter(user=usr).count()
        categories = CategoryModel.objects.all()
        context = {'form': form,'cart_count':cart_count,'categories':categories}
    return render(request, 'profile.html', context)


def AddressView(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        address = CustomerModel.objects.filter(user=request.user)
        usr = request.user
        cart_count = Cart.objects.filter(user=usr).count()
        categories = CategoryModel.objects.all()
        if form.is_valid():
            usr = request.user
            name = form.cleaned_data['name']
            mobile = form.cleaned_data['mobile']
            email = form.cleaned_data['email']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            zipcode = form.cleaned_data['zipcode']
            state = form.cleaned_data['state']
            data = CustomerModel(
                user=usr,
                name=name,
                mobile=mobile,
                email=email,
                locality=locality,
                city=city,
                zipcode=zipcode,
                state=state,
            )
            data.save()
            messages.info(request, 'Address Successfully Added...!')
            form = CustomerForm()
        context = {'form': form, 'address': address,'cart_count':cart_count,'categories':categories}
        return render(request, 'address.html', context)
    else:
        form = CustomerForm()
        address = CustomerModel.objects.filter(user=request.user)
        usr = request.user
        cart_count = Cart.objects.filter(user=usr).count()
        categories = CategoryModel.objects.all()
    context = {'form': form, 'address': address,'cart_count':cart_count,'categories':categories}
    return render(request, 'address.html', context)


def CahngePassView(request):
    if request.method == 'POST':
        usr = request.user
        # cart_count = Cart.objects.filter(user=usr).count()
        categories = CategoryModel.objects.all()
        form = PassChangeForm(data=request.POST,user=usr)
        if  form.is_valid():
            form.save()
            messages.success(request,'Password Successfully Changed')
            return redirect('/changepass/')
    else:
        usr = request.user
        cart_count = Cart.objects.filter(user=usr).count()
        categories = CategoryModel.objects.all()
        form = PassChangeForm(user=usr)
    context = {'form':form,'cart_count':cart_count,'categories':categories}
    return render(request, 'changepass.html',context)


def OrdersView(request):
    if request.method == 'POST':
        user = request.user
        address_id = request.POST.get('address_id')
        customer_data = CustomerModel.objects.get(id=address_id)
        cart_data = Cart.objects.filter(user=user)
        categories = CategoryModel.objects.all()
        productamount = 0
        shipping_amt = 40
        final_amt = 0
        for i in cart_data:
            prod_amt = ((i.product.price)*(i.quantity))
            productamount += prod_amt
            final_amt = productamount+shipping_amt
        # Pament Start
        ok = (final_amt)*100
        client = razorpay.Client(auth=("rzp_test_Vmt3z0OcBPopoR", "N00ygDuM1UXU8Xp8Qfde9dOE"))
        payment = client.order.create({'amount': ok, 'currency': 'INR','payment_capture': '1'})
        # Pament End             
        for i in cart_data:
            order_data = Order(
                user=user,
                customer=customer_data,
                product=i.product,
                quantity=i.quantity,
            )
            order_data.save()
            messages.success(request,'Your Order Successfully Placed Thank you shoping With us')
        cart_data.delete()
        return redirect('/showorders/')
    else:
        pass


def OrderShow(request):
    order_data = Order.objects.filter(user=request.user)[::-1]
    order_count = Order.objects.filter(user=request.user).count()
    usr = request.user
    cart_count = Cart.objects.filter(user=usr).count()
    categories = CategoryModel.objects.all()
    return render(request,'orders.html',{'order_data':order_data,
    'order_count':order_count,'cart_count':cart_count,'categories':categories})

def CheckoutView(request):
    usr = request.user
    cutomer_data = CustomerModel.objects.filter(user=usr)
    product_data = Cart.objects.filter(user=usr)
    cart_count = Cart.objects.filter(user=usr).count()
    productamount = 0
    shipping_amt = 40
    final_amt = 0
    data = Cart.objects.filter(user=usr)
    for i in product_data:
        prod_amt = ((i.product.price)*(i.quantity))
        productamount += prod_amt
        final_amt = productamount+shipping_amt
    # Pament Start
    client = razorpay.Client(auth=("rzp_test_Vmt3z0OcBPopoR", "N00ygDuM1UXU8Xp8Qfde9dOE"))
    payment = client.order.create({'amount':(final_amt)*100, 'currency': 'INR','payment_capture': '1'})
    # Pament End 
    context = {'cutomer_data': cutomer_data, 'product_data': product_data,
               'productamount': productamount, 'shipping_amt': shipping_amt, 
               'final_amt': final_amt,'cart_count':cart_count,'payment':payment}
    return render(request, 'checkout.html', context)


def ProductDetailsView(request, id):
    product = ProductModel.objects.filter(id=id)
    user = request.user
    # already_in_cart = False
    categories = CategoryModel.objects.all()
    already_in_cart = Cart.objects.filter(Q(user=user) & Q(product_id=id)).exists()
    context = {'product': product,'already_in_cart':already_in_cart,'categories':categories}
    return render(request, 'productdetails.html', context)


def AllProductView(request):
    products = ProductModel.objects.all()
    categories = CategoryModel.objects.all()
    usr = request.user
    cart_count = Cart.objects.filter(user=usr).count()
    data = list(request.GET)
    categories = CategoryModel.objects.all()
    for i in data:
        if int(i) == None:
            products = ProductModel.objects.all()
        else:
            products = ProductModel.objects.filter(category_id=i)

    context = {'products': products, 'categories': categories, 'cart_count':cart_count}
    return render(request, 'allproducts.html', context)


# -------------------------------------------------------------------------------
#                              Auth Section
# -------------------------------------------------------------------------------

# User Login
def SigninView(request):
    form = SigninForm()
    if request.method == 'POST':
        uname = request.POST['uname']
        upass = request.POST['upass']
        user = authenticate(username=uname, password=upass)
        if user is None:
            messages.error(request, 'Please Enter Correct Credinatial')
            return redirect('/signin/')
        else:
            login(request, user)
            messages.info(request, 'Login Successful')
            return redirect('/shop/')
    else:
        if request.user.is_authenticated:
            return redirect('/shop/')
        else:
            return render(request, 'login.html', {'form': form})
# Logout


def Userlogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, '🙋‍ You are Successfully Logged Out !')
    return redirect('/')


# User Register
def UserRegisterView(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            form.save()
            messages.success(request, f'{uname} - User Successfully Registred')
            form = UserCreateForm()
            context = {'form': form}
            return render(request, 'signup.html', context)
    else:
        form = UserCreateForm()
    context = {'form': form}
    return render(request, 'signup.html', context)


# TEST KEY : rzp_test_3TgO7ZbqAF1dN1
# TEST ID : eONIoTp17Y0eAGU0UTuJ0C44
