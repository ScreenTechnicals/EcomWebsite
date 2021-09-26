from django.shortcuts import redirect, render
from .models import Pizza, Orders
from django.contrib.auth.models import User
# Create your views here.
def home(request):
    pizza = Pizza.objects.all()
    last = pizza[len(pizza)-1]
    second_last = pizza[len(pizza)-2]
    third_last = pizza[len(pizza)-3]
    forth_last = pizza[len(pizza)-4]
    user = User.objects.all().first()
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
    user = User.objects.all().first()
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
    user = User.objects.all().first()
    order = Orders.objects.filter(User=user)
    total_pizzas = len(order)
    context = {
        'pizzas':pizzas,
        'total_pizzas':total_pizzas,
    }
    if request.method == 'POST':
        sno = request.POST['sno']
        pizza_ = Pizza.objects.filter(sno=sno).first()
        p_name = pizza_.Pizza_name
        p_desc = pizza_.Pizza_desc
        p_price = pizza_.Pizza_price

        # print(p_name)
        user = User.objects.all().first()
        orders = Orders(Pizza_name=p_name, Pizza_desc=p_desc, Pizza_price=p_price, User = user)
        orders.save()
        return redirect("/menu/")
    return render(request, "Home/menu.html", context)
