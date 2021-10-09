from django.forms import ModelForm
from django.http import request
from .models import Profile
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['User']
