

from django import forms
from django.contrib.auth.models import User

from .models import Product, Orders


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'in_stock', 'category']


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput)
    email = forms.CharField(label='Введите Email', widget=forms.TextInput)
    password = forms.CharField(label='Введите пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)


    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError("Пароли не совпадают")
        return cleaned_data

class OrderForm(forms.ModelForm):
    class Meta:
        model = Orders
        fields = ['address', 'phone']
        widgets = {
            'address': forms.TextInput(attrs={
                'placeholder': 'Введите адрес доставки',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Введите номер телефона',
                'class': 'form-control'
            }),
        }

