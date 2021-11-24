from django.shortcuts import redirect, render
from .models import Address, Contact, Pizza, Orders, Profile
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import ProfileForm
from django.contrib.auth.models import AnonymousUser
# Create your views here.
def home(request):
    pizza = Pizza.objects.all()
    last = pizza[len(pizza)-1]
    second_last = pizza[len(pizza)-2]
    third_last = pizza[len(pizza)-3]
    forth_last = pizza[len(pizza)-4]
    # Total Num Of Orders
    current_user = request.user
    if request.user and request.user != AnonymousUser():
        ordersOfCurrentUser = Orders.objects.filter(User=current_user)
        totalOrdersList = []
        for pizzaOrder in ordersOfCurrentUser:
            quantity = pizzaOrder.quantity
            totalOrdersList.append(quantity)
        
        totalOrders = sum(totalOrdersList)
    else:
        totalOrders = 0
        

    context = {
        'pizza': pizza,
        'last': last,
        'second_last': second_last,
        'third_last':third_last,
        'forth_last':forth_last,
        'totalOrders': totalOrders,
    }
    return render(request, "Home/index.html", context)


def orders(request):
    current_username = request.user.username
    user = User.objects.filter(username=current_username).first()
    order = Orders.objects.filter(User=user)
    # print(order)

    price_list = []
    for pizza in order:
        price = pizza.Pizza_price
        price_list.append(price)

    total_price = round(sum(price_list), 3)
    # Total Num Of Orders
    if request.user and request.user != AnonymousUser():

        current_user = request.user
        ordersOfCurrentUser = Orders.objects.filter(User=current_user)
        totalOrdersList = []
        for pizzaOrder in ordersOfCurrentUser:
            quantity = pizzaOrder.quantity
            totalOrdersList.append(quantity)
        
        totalOrders = sum(totalOrdersList)
        firstobjectofcurrentuser = ordersOfCurrentUser.first()
    else:
        totalOrders = 0
    

    context = {
        'order':order,
        'total_price':total_price,
        'totalOrders':totalOrders,
        'firstobjectofcurrentuser':firstobjectofcurrentuser,
    }
    return render(request, "Home/orders.html", context)

def increament(request):
    if request.method == "POST":
        orderId = request.POST['order_Id']
        order = Orders.objects.filter(id=orderId)
        order_ = Orders.objects.filter(id=orderId).first()
        pizzaPrice = order_.Pizza_price

        if order_.quantity == 0:
            order.update(quantity=1)
            return redirect("/orders/")
        else:
            order_.quantity += 1
            order.update(quantity=order_.quantity)
            pizzaPrice = round(pizzaPrice * order_.quantity, 3)
            order.update(Pizza_price=pizzaPrice)
            return redirect("/orders/")

                
def decreament(request):
    if request.method == "POST":
        orderId = request.POST['order_Id']
        Pizza_name_ = request.POST['Pizza_name_']
        order = Orders.objects.filter(id=orderId)
        order_ = Orders.objects.filter(id=orderId).first()
        pizzaPrice = order_.Pizza_price

        if order_.quantity == 1:
            order.update(quantity=0)
            order.delete()
            return redirect("/orders/")
            
        else:
            order_.quantity -= 1
            order.update(quantity=order_.quantity)
            pizzaPrice = Pizza.objects.filter(Pizza_name=Pizza_name_).first().Pizza_price
            pizzaPrice = round(pizzaPrice * order_.quantity, 3)
            order.update(Pizza_price=pizzaPrice)
            return redirect("/orders/")

        
def menu(request):
    try:
        if request.user:    
            pizzas = Pizza.objects.all() 
            current_username = request.user.username
            user = User.objects.filter(username=current_username).first()
            order = Orders.objects.filter(User=user)
            # Total Num Of Orders
            if request.user and request.user != AnonymousUser():
                current_user = request.user
                ordersOfCurrentUser = Orders.objects.filter(User=current_user)
                totalOrdersList = []
                for pizzaOrder in ordersOfCurrentUser:
                    quantity = pizzaOrder.quantity
                    totalOrdersList.append(quantity)
                
                totalOrders = sum(totalOrdersList)
            else:
                totalOrders = 0
            ordersOfCurrentUser = Orders.objects.filter(User=request.user)
            firstobjectofcurrentuser = ordersOfCurrentUser.first()
            context = {
                'pizzas':pizzas,
                'totalOrders':totalOrders,
                'firstobjectofcurrentuser':firstobjectofcurrentuser,
            }
            # Taking Oreders
            try:
                if request.method == 'POST':
                    sno = request.POST['sno']
                    pizza_ = Pizza.objects.filter(sno=sno).first()
                    p_name = pizza_.Pizza_name
                    p_desc = pizza_.Pizza_desc
                    p_price = pizza_.Pizza_price
                    
                    if not Address.objects.filter(User=request.user):
                        messages.success(request, "Please provide a address !")
                        return redirect("/profile/")
                    else:
                        """to handle quantity in menu"""
                        allorders = Orders.objects.filter(User=request.user, Pizza_name=p_name)

                        if not allorders:
                            orders = Orders(Pizza_name=p_name, Pizza_desc=p_desc, Pizza_price=p_price, User = user)
                            orders.save()
                            return redirect("/menu/")
                        else:
                            order_ = Orders.objects.filter(User=request.user, Pizza_name=p_name)
                            order_quantity = order_.first().quantity
                            if order_quantity == 0:
                                order_.update(quantity=1)
                                return redirect("/menu/")
                            else:
                                order_quantity += 1
                                order_.update(quantity=order_quantity)
                                return redirect("/menu/")

            except Exception as e:
                return redirect("/login/")

            return render(request, "Home/menu.html", context)
        else:
            # msg
            return redirect("/login/")
    except Exception:
        messages.success(request, "Login To Continue!")
        return redirect("/login/")

def signup(request):
    current_username = request.user.username
    user = User.objects.filter(username=current_username).first()
    order = Orders.objects.filter(User=user)
    total_pizzas = len(order)
    context = {
        'total_pizzas':total_pizzas,
    }
    if request.method == "POST":
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        user_name = request.POST['user_name']
        user_email = request.POST['user_email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if pass1 == pass2:
            if User.objects.filter(username=user_name).exists() and User.objects.filter(email=user_email).exists():
                messages.warning(request, "Username and Email are already taken")

            elif User.objects.filter(username=user_name).exists():
                messages.warning(request, "Username already taken")

            elif User.objects.filter(email=user_email).exists():
                messages.warning(request, "Email already taken")
            else:
                user = User.objects.create_user(user_name, user_email, pass1)
                user.first_name = f_name
                user.last_name = l_name
                user.save()
                user_login = auth.authenticate(username=user_name, password=pass1)
                if user_login is not None:
                    auth.login(request, user_login)
                    messages.success(request, "Successfully Logged In !")
                    return redirect("/")
                else:
                    messages.success(request, "Invalid Sign Up Inputs Given !")
                    

        else:
            messages.warning(request, "Create Password and Confirmed Password Don't Match")

    return render(request, "Home/signup.html", context)
    
def login(request):
    current_username = request.user.username
    user = User.objects.filter(username=current_username).first()
    order = Orders.objects.filter(User=user)
    total_pizzas = len(order)
    context = {
        'total_pizzas':total_pizzas,
    }
    if request.method == "POST":
        user_name_ = request.POST['user_name_']
        pass_ = request.POST['pass_']
        user_login = auth.authenticate(username=user_name_, password=pass_)
        if user_login is not None:
            auth.login(request, user_login)
            messages.success(request, "Successfully Logged In !")
            return redirect("/")
        else:
            messages.warning(request, "Sign up First")

    return render(request, "Home\login.html", context)

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect("/")

def profile(request):
    try:
        if request.user:
            # Total no of orders by the logedin user
            current_username = request.user.username
            user = User.objects.filter(username=current_username).first()
            order = Orders.objects.filter(User=user)
            # total_pizzas = len(order)
            # Total Num Of Orders
            if request.user and request.user != AnonymousUser():
                current_user = request.user
                ordersOfCurrentUser = Orders.objects.filter(User=current_user)
                totalOrdersList = []
                for pizzaOrder in ordersOfCurrentUser:
                    quantity = pizzaOrder.quantity
                    totalOrdersList.append(quantity)
                
                totalOrders = sum(totalOrdersList)
            else:
                totalOrders = 0
            # current user object
            current_user = request.user
            # Profile Image Upload and Update Handling
            form = ProfileForm(instance=current_user)
            if request.method == "POST":
                try:
                    profile_Image=request.FILES['profile_Image']
                    profile = Profile(User=current_user, profile_Image=profile_Image)
                    profile.save()
                except Exception as e:
                    return redirect("/profile/")

            profile_objects = Profile.objects.filter(User=request.user)
            if profile_objects:
                profile_iamge_display = Profile.objects.filter(User=current_user).last()
                profile_iamge_display_url = profile_iamge_display.profile_Image 
            else:
                profile_iamge_display_url = "images/defaultuser.png"

            # Address show
            address = Address.objects.filter(User = current_user).first()   
            if address: 
                address_display = address.address
            else:
                address_display = "No Address, Please Add!"

            context = {
                'profile_iamge_display_url':profile_iamge_display_url,
                'form':form,
                'totalOrders':totalOrders,
                'address_display':address_display,
            }
                    
            return render(request, "Home/profile.html", context)
        else:
            return redirect("/")
    except Exception:
        return redirect("/")
        
def address(request):
    # Address handling
    # current user object
    current_user = request.user
    if request.method == "POST":
        address_ = request.POST['address_area']
        if not Address.objects.filter(User=current_user).first():    
            address = Address(User=current_user, address=address_)
            address.save()
            messages.success(request, "Address Saved !")
        else:
            address = Address.objects.filter(User=current_user).update(address=address_)
            messages.success(request, "Address Updated !")
            
        return redirect("/profile/")

def deleteOrder(request):
    if request.method == "POST":
        orderId = request.POST['order_id']
        orderToBeDeleted = Orders.objects.get(id=orderId)
        orderToBeDeleted.delete() 
        return redirect("/orders/")

def deleteAllOrder(request):
    if request.method == "POST":
        # current user object
        current_user = request.user
        allOrders = Orders.objects.filter(User=current_user)
        # print(allOrders)
        allOrders.delete()
        return redirect("/orders/")
        

def orderConfirmed(request):
    if request.method == "POST":
        # current user object
        current_user = request.user
        allOrders = Orders.objects.filter(User=current_user).update(order_confirmed=True)
        return redirect("/orders/")
        

def contact(request):
    try:
        if request.user:
            if request.method == "POST":
                query_details = request.POST["query_details"]
                if request.user and request.user != AnonymousUser(): 
                    current_user = request.user
                    contact = Contact(User=current_user, query=query_details)
                    contact.save()
                    # message
                else:
                    # message
                    pass
            return render(request, "Home/contact.html")
        else:
            return redirect("/login/")    
    except Exception:
        # message
        return redirect("/login/")    