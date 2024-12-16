from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Order, Customer, Employe


class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = "__all__"


class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = "__all__"
        exclude = ['user']


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class CreateNewUser(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'your-class-name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Your Email', 'class': 'your-class-name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'your-class-name'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password', 'class': 'your-class-name'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class Empolye(ModelForm):
    class Meta:
        model = Employe
        fields = "__all__"
