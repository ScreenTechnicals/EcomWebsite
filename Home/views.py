from django.shortcuts import render
from .models import Pizza
# Create your views here.
def home(request):
    pizza = Pizza.objects.all()
    last = pizza[len(pizza)-1]
    second_last = pizza[len(pizza)-2]
    third_last = pizza[len(pizza)-3]
    forth_last = pizza[len(pizza)-4]
    context = {
        'pizza': pizza,
        'last': last,
        'second_last': second_last,
        'third_last':third_last,
        'forth_last':forth_last,
    }
    return render(request, "Home/index.html", context)