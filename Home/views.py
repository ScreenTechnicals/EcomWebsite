from django.forms.utils import pretty_name
from django.shortcuts import redirect, render
from .models import Pizza, Orders, Profile
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .forms import ProfileForm
# Create your views here.
def home(request):
    pizza = Pizza.objects.all()
    last = pizza[len(pizza)-1]
    second_last = pizza[len(pizza)-2]
    third_last = pizza[len(pizza)-3]
    forth_last = pizza[len(pizza)-4]
    current_username = request.user.username
    user = User.objects.filter(username=current_username).first()
    order = Orders.objects.filter(User=user)
    total_pizzas = len(order)

    context = {
        'pizza': pizza,
        'last': last,
        'second_last': second_last,
        'third_last':third_last,
        'forth_last':forth_last,
        'total_pizzas':total_pizzas,
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
    # print(price_list)
    total_price = round(sum(price_list), 3)
    # print(total_price)
    total_pizzas = len(order)
    context = {
        'order':order,
        'total_price':total_price,
        'total_pizzas':total_pizzas,
    }
    return render(request, "Home/orders.html", context)


def menu(request):
    pizzas = Pizza.objects.all() 
    current_username = request.user.username
    user = User.objects.filter(username=current_username).first()
    order = Orders.objects.filter(User=user)
    total_pizzas = len(order)
    context = {
        'pizzas':pizzas,
        'total_pizzas':total_pizzas,
    }
    # Taking Oreders
    if request.method == 'POST':
        sno = request.POST['sno']
        pizza_ = Pizza.objects.filter(sno=sno).first()
        p_name = pizza_.Pizza_name
        p_desc = pizza_.Pizza_desc
        p_price = pizza_.Pizza_price

        
        current_username = request.user.username
        user = User.objects.filter(username=current_username).first()
        orders = Orders(Pizza_name=p_name, Pizza_desc=p_desc, Pizza_price=p_price, User = user)
        orders.save()
        return redirect("/menu/")
    return render(request, "Home/menu.html", context)


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

    return render(request, "Home\login.html")

def logout(request):
    if request.method == "POST":
        auth.logout(request)
        return redirect("/")

def profile(request):
    current_user = request.user
    
    form = ProfileForm(instance=current_user)
    if request.method == "POST":
        profile = Profile(User=current_user, profile_Image=request.FILES['profile_Image'])
        profile.save()

    profile_objects = Profile.objects.filter(User=request.user)
    if profile_objects:
        profile_iamge_display = Profile.objects.filter(User=current_user).last()
        profile_iamge_display_url = profile_iamge_display.profile_Image 
    else:
        profile_iamge_display_url = "images/defaultuser.png"
    
    context = {
        'profile_iamge_display_url':profile_iamge_display_url,
        'form':form,
    }
            
    return render(request, "Home/profile.html", context)