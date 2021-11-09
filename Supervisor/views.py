from django.shortcuts import redirect, render
from django.contrib.auth.models import User, auth
from Home.models import Address, Contact, Pizza, Orders, Profile

# Create your views here.

def dashboard(request):
    if request.user.is_superuser:
        allconfirmedorders = Orders.objects.filter(order_confirmed=True)
        # allusers = User.objects.filter(is_superuser=False, username=user.User.username)
        context = {
            # "allusers":allusers,
            "allconfirmedorders":allconfirmedorders,
        }
        return render(request, "Supervisor/dashboard.html", context)
    else:
        return redirect("/")

def contactlist(request):
    if request.user.is_superuser:
        contacts = Contact.objects.all()
        # print(contacts.first().id)
        context = {
            "contacts":contacts,
        }
        return render(request, "Supervisor/contactlist.html", context)
    else:
        return redirect("/")

def contact_view(request, id):
    if request.user.is_superuser:
        contacts = Contact.objects.filter(id=id)
        context = {
            "contacts":contacts,
        }
        if request.method=="POST":
            c_id = request.POST['c_id']
            contact = Contact.objects.filter(id=c_id)
            contact.delete()
            return redirect("/contactlist/")
        return render(request, "Supervisor/contact_view.html", context)
    else:
        return redirect("/")


def order_view(request, id):
    if request.user.is_superuser:
        orders = Orders.objects.filter(id=id)
        address = Address.objects.all()
        profile_images = Profile.objects.all()
        context = {
            "orders": orders,
            "address":address,
            "profile_images": profile_images,
        }
        if request.method=="POST":
            o_id = request.POST['o_id']
            order = Orders.objects.filter(id=o_id)
            order.delete()
            # message
            return redirect("/dashboard/")
        return render(request, "Supervisor/order_view.html", context)
    else:
        return redirect("/")


def search_order(request):
    if request.user.is_superuser:
        search = request.GET['search']
        # username = Orders.objects.filter(User__icontains=search)
        pizza_name = Orders.objects.filter(Pizza_name__icontains=search)
        pizza_desc = Orders.objects.filter(Pizza_desc__icontains=search)
        pizza_price = Orders.objects.filter(Pizza_price__icontains=search)
        union_one = pizza_name.union(pizza_desc)
        allsearches = union_one.union(pizza_price)
        # allsearches = union_two.union(username)
        context = {
            'allsearches':allsearches,
        }
        return render(request, "Supervisor/search.html", context)
    else:
        return redirect("/")

