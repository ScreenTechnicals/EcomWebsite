from django.contrib import admin
from .models import Contact, Pizza, Orders, Profile, Address
# Register your models here.
admin.site.register(Pizza)
admin.site.register(Orders)
admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(Contact)
