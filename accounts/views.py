from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from accounts.models import AddProductModel, PlaceOrderModel
from .forms import AddProductForm


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_staff == 1:
                return redirect('admin-dashboard')
            else:
                return redirect('user-dashboard')

        else:
            messages.info(request, 'invalid credentials')
            print('invalid credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'Username taker')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email,
                                                first_name=first_name, last_name=last_name)
                user.save()
                print('user created')
                return redirect('login')

        else:
            messages.info(request, 'Password not matching')
            return redirect('register')

    else:
        return render(request, "register.html")


def adminDashboard(request):
    allUserDetails = User.objects.all()
    orderDetail = PlaceOrderModel.objects.all()
    context = {'orderDetail': orderDetail, 'allUserDetails': allUserDetails}
    return render(request, 'admin-dashboard.html', context)


def showUserDetail(request, id):
    userDetail = User.objects.get(pk=id)
    return render(request, "user-profile-order.html", {'userDetail': userDetail})


def delete(request, id):
    deleteProduct = AddProductModel.objects.get(pk=id)
    deleteProduct.delete()
    return redirect("show-product-details")


def addProduct(request):
    return render(request, 'add-product.html')


def saveProduct(request):
    if request.method == 'POST':
        if request.POST.get('product_name') and request.POST.get('product_quantity') and request.POST.get(
                'product_price'):
            addProductModel = AddProductModel()
            addProductModel.product_name = request.POST['product_name']
            addProductModel.product_description = request.POST['product_description']
            addProductModel.product_price = request.POST['product_price']
            addProductModel.product_quantity = request.POST['product_quantity']

            addProductModel.save()
            return redirect('show-product-details')


def showProductDetails(request):
    dests = AddProductModel.objects.all()
    return render(request, 'show-product-details.html', {'dests': dests})


def userDashboard(request):
    return render(request, 'user-dashboard.html')


def showAvailableProd(request):
    dests = AddProductModel.objects.all()
    return render(request, 'show-available-products.html', {'dests': dests})


def add(request):
    form = AddProductForm()
    if request.method == 'POST':
        form = AddProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('show-product-details')

    context = {'form': form}
    return render(request, 'add.html', context)


def update(request, pk):
    add = AddProductModel.objects.get(id=pk)
    form = AddProductForm(instance=add)
    if request.method == 'POST':
        form = AddProductForm(request.POST, instance=add)
        if form.is_valid():
            form.save()
            return redirect('show-product-details')

    context = {'form': form}
    return render(request, 'add.html', context)


def placeOrder(request, id):
    username = request.user
    productDetail = AddProductModel.objects.get(pk=id)
    context = {'productDetail': productDetail, 'username': username}
    if request.method == 'POST':
        if request.POST.get('product_quantity'):
            orderModel = PlaceOrderModel()
            orderModel.product_name = request.POST['product_name']
            orderModel.product_description = request.POST['product_description']
            orderModel.product_price = request.POST['product_price']
            orderModel.order_by = request.POST['order_by']
            orderModel.product_quantity = request.POST['product_quantity']
            orderModel.product_status = request.POST['product_status']

            orderModel.save()
            return redirect('user-dashboard')
    return render(request, 'place-order.html', context)

    # productDetail = AddProductModel.objects.get(pk=id)
    # username = request.user
    # print(str(productDetail) + "==================")
    # form = PlaceOrderForm()
    # if request.method == 'POST':
    #     form = PlaceOrderForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return redirect('user-dashboard')
    #
    # context = {'placeForm': form, 'productDetail': productDetail, 'username': username}
    # return render(request, 'place-order.html', context)


def showOrderHistory(request):
    username = request.user
    orderDetail = PlaceOrderModel.objects.filter(order_by=username)
    print(orderDetail)
    context = {'orderDetail': orderDetail}

    return render(request, 'order-history.html', context)


def updateStatus(request):
    username = request.user
    PlaceOrderModel.objects.filter(order_by=username).filter(product_status='Active').update(product_status='Completed')
    # PlaceOrderModel.objects.filter(order_by=username).filter(product_status='Placed').update(product_status='Active')
    return HttpResponse("Status Updated")
