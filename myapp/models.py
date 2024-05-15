from django.db import models

# Create your models here.


class Client(models.Model): # создание модели Client.
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)# уникальное поле, не может быть одинаковых email
    phone = models.CharField(max_length=16) #+7(999)999-99-99
    address = models.CharField(max_length=100)
    reg_data = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='clients/', null=True, blank=True)  # добавляем поле для изображения

    def __str__(self):
        return f'Имя клиента: {self.name}, Электронная почта: {self.email}'


'''
Поля модели «Product»:
— название товара
— описание товара
— цена товара
— количество товара
— дата добавления товара
'''
# HW-4 25.04.24
class Product(models.Model): # создание модели Product.
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default='cloth') # категория товара
    description = models.TextField() # Описание товара
    price = models.DecimalField(max_digits=10, decimal_places=2) # decimal_places - количество знаков после запятой
    quantity = models.IntegerField() # количество товара
    add_data = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)  # добавляем поле для изображения
    active = models.BooleanField(default=True) # активный товар или нет

    def __str__(self):
        return f'Название товара: {self.name}, Цена товара: {self.price}'

    def total_price(self):
        return self.price * self.quantity

# HW-4 25.04.24
# Модель ProductImage для хранения изображений товаров
# для каждого товара может быть несколько изображений
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')

class ProductCategory(models.Model):
    '''Модель категории товара'''
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'Категория товара: {self.name}'


'''
Поля модели «Order»:
— связь с моделью «Клиент», указывает на клиента, сделавшего заказ
— связь с моделью «Товар», указывает на товары, входящие в заказ
— общая сумма заказа
— дата оформления заказа
'''

class Order(models.Model): # создание модели Order.
    client = models.ForeignKey(Client, on_delete=models.CASCADE) # если удаляется клиент, то удаляется и заказ
    product = models.ManyToManyField(Product) # связь многое ко многим - один заказ может содержать несколько товаров
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_data = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default=1) # количество товаров в заказе, по умолчанию 1


    def __str__(self):
        return f'Заказ клиента: {self.client}, Общая сумма заказа: {self.total_price} дата заказа: {self.order_data}'


    # Товары в заказе
    def get_products(self):
        order_products = Product.objects.filter(order=self)
        if order_products:
            return f'Товары в заказе: {order_products}'
        else:
            return f'В заказе нет товаров'


#--------------------------------------------------------------
'''Важно не забыть сделать миграцию после создания новой модели.'''
# Для этого выполните команду: py manage.py makemigrations myapp
# Для применения миграции выполните команду: py manage.py migrate

