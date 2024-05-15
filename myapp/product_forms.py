from django import forms
from .models import Product
from django.core.exceptions import ValidationError # импорт исключения ValidationError
from .constants import CATEGORY_CHOICES

'''Форма для добавления товара'''

ACTIVE_CHOICES = [
    (True, 'Активный'),
    (False, 'Неактивный'),
]

class ProductForm(forms.Form):
    name = forms.CharField(label='Наименование товара', min_length=3, max_length=100, required=True) # required=True - поле обязательное
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, label='Категория товара') # виджет выпадающего списка
    description = forms.CharField(label='Описание товара', widget=forms.Textarea, required=True) # widget=forms.Textarea - поле для ввода текста
    price = forms.DecimalField(label='Цена товара', max_digits=1_000_000, decimal_places=2, required=True) # decimal_places - количество знаков после запятой
    quantity = forms.IntegerField(label='Количество товара', max_value=1_000_000, required=True) # max_value - максимальное значение
    image = forms.ImageField(label='Загрузите изображения', required=False) # required=False - поле не обязательное
    active = forms.ChoiceField(choices=ACTIVE_CHOICES, widget=forms.RadioSelect(attrs={'class': 'inline'}), initial=True, label='Активный товар') # виджет радиокнопок

    def clean_name(self):
        name = self.cleaned_data['name']
        if Product.objects.filter(name=name).exists(): #.exists() - проверка на существование
            raise forms.ValidationError('Товар с таким наименованием уже существует')
        return name


    def clean_image(self):
        image = self.cleaned_data['image']
        if image:
            if image.size > 2*1024*1024: # размер изображения в байтах
                raise ValidationError('Размер изображения не должен превышать 2 Мб')
            return image
        else:
            return image # если изображение не загружено, возвращаем None


