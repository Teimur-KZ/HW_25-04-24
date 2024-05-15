import datetime
from django import forms
from .models import Client

'Форма для добавления клиента'

class ClientForm(forms.Form):
    name = forms.CharField(label='Имя клиента', min_length=3, max_length=50, required=True)
    email = forms.EmailField(label='Электронная почта', max_length=100, required=True)
    phone = forms.CharField(label='Телефон',min_length=11, max_length=16, required=True) #+7(999)999-99-99
    address = forms.CharField(label='Адрес', max_length=100, required=True)
    image = forms.ImageField(label='Загрузите изображение', required=False) #required=False - поле не обязательное

    def clean_name(self):
        name = self.cleaned_data['name']
        if name.lower() == 'admin':
            raise forms.ValidationError('Имя не может быть admin')
        return name

    def clean_email(self):
        email = self.cleaned_data['email']
        if Client.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email