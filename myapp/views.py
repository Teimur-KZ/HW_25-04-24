from django.shortcuts import render

# Create your views here.
# HW-3 22.04.24
# HW-4 25.04.24
import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from datetime import datetime, timedelta
import django.utils.timezone
from .user_forms import ClientForm
from .product_forms import ProductForm
from .models import Client, Order, Product
from .constants import CATEGORY_CHOICES


logger = logging.getLogger(__name__) # создание объекта логгера

# Представление главной страницы
def index(request): # определение представления index
    logger.info('Страница "Главная страница" была посещена') # запись сообщения в лог
    html = """
    <h1>Главная страница</h1>
    <p>Фреймворк Django - Урок 4. Работа с Формами HW-4 25.04.24</p>
    <p>Задание:</p>
    <p>    
    Измените модель продукта, добавьте поле для хранения фотографии продукта.
    <p>Создайте форму, которая позволит сохранять фото.</p>
    """
    title = "Главная страница"
    return render(request, 'index.html', {'html': html, 'title': title}) # возврат ответа

# Представление "О себе"
def about(request):
    # Логирование данных о посещении страницы
    logger.info('Страница "О себе" была посещена')

    html = """
    <h1>Обо мне</h1>
    <p>Информация о себе....</p>
    <p>Меня зовут Теймур - это домашнее задание по Django.</p>
    """
    title = "О себе"
    return render(request, 'about.html', {'html': html, 'title': title})

# Обработчик ошибки 404
def error_404(request, exception):
    #return render(request, '404.html', status=404) или так:
    logger.error(f'Страница не найдена')
    title = 'Страница не найдена'
    return render(request, '404.html', {'title': title}, status=404)

#HW-3 22.04.24
def client_orders_post(request, client_id):
    client = get_object_or_404(Client, pk=client_id)
    orders = Order.objects.filter(client=client)
    request.session['client_id'] = client_id # сохраняем id клиента в сессии, что бы мог вернуться на страницу клиента из товара

    # Получаем текущую дату и время
    #now = datetime.now()
    now = django.utils.timezone.now()

    # Создаем словарь для хранения товаров за разные периоды времени
    products_by_time = {
        'week': set(),
        'month': set(),
        'year': set(),
        'count_orders_week': 0,
        'count_orders_month': 0,
        'count_orders_year': 0,
        'sum_orders_week': 0,
        'sum_orders_month': 0,
        'sum_orders_year': 0,
    }

    # Проходим по каждому заказу
    for order in orders:
        # Получаем товары из заказа
        products = Product.objects.filter(order=order)

        # Сортируем товары по времени и добавляем в соответствующие списки
        for product in products:
            if order.order_data >= now - timedelta(days=7):
                products_by_time['week'].add(product)
                products_by_time['count_orders_week'] += 1
                products_by_time['sum_orders_week'] += order.total_price * order.quantity # сумма заказа за неделю
            elif order.order_data >= now - timedelta(days=30):
                products_by_time['month'].add(product)
                products_by_time['count_orders_month'] += 1
                products_by_time['sum_orders_month'] += order.total_price * order.quantity # сумма заказа за месяц
            elif order.order_data >= now - timedelta(days=365):
                products_by_time['year'].add(product)
                products_by_time['count_orders_year'] += 1
                products_by_time['sum_orders_year'] += order.total_price * order.quantity # сумма заказа за год

    #print(products_by_time, 'products_by_time') # вывод в консоль - проверка
    return render(request, 'client_orders.html', {'client': client, 'products_by_time': products_by_time, 'orders': orders})

#HW-3 22.04.24
def product_full(request, product_id):
    product = get_object_or_404(Product, pk=product_id) # объект товара по его id
    client_id = request.session.get('client_id')
    client = get_object_or_404(Client, pk=client_id) # объект клиента по его id
    order = Order.objects.filter(product=product, client=client).first()
    return render(request, 'product_about.html',
                  {'product': product, 'client': client, 'title': 'Полный товар', 'price': product.price,
                   'add_data': product.add_data, 'order': order})

# HW-3 22.04.24
def clients_all(request):
    '''Отображение всех клиентов'''
    clients = Client.objects.all()
    return render(request, 'clients_all.html', {'clients': clients, 'title': 'Список клиентов'})

# HW-3 22.04.24
def client_about(request, client_id):
    '''Отображение информации о клиенте'''
    client = get_object_or_404(Client, pk=client_id)
    return render(request, 'client_about.html', {'client': client, 'title': 'Информация о клиенте'})

# HW-4 25.04.24
def add_user(request):
    '''Добавление нового пользователя'''
    if request.method == 'POST':
        form = ClientForm(request.POST, request.FILES) # создаем форму с данными из запроса
        message = 'Ошибка в данных формы'
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            image = form.cleaned_data['image'] if form.cleaned_data['image'] else 'clients/blank.jpg'
            logger.info(f'Получили данные: {name}, {email}, {phone}, {address}')
            user = Client(name=name, email=email, phone=phone, address=address, image=image)
            user.save()
            #message = f'Пользователь {name} добавлен'
            messages.success(request, f'Пользователь {name} добавлен')
            return redirect('clients_all')

    else:
        form = ClientForm()
        message = 'Введите данные пользователя'
    return render(request, 'add_user.html', {'form': form, 'message': message})



# HW-4 25.04.24
def add_product(request):
    '''Добавление нового товара'''
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        message = 'Ошибка в данных формы'
        if form.is_valid():
            name = form.cleaned_data['name']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            quantity = form.cleaned_data['quantity']
            image = form.cleaned_data['image'] if form.cleaned_data['image'] else 'products/blank.jpg'
            active = form.cleaned_data['active']
            logger.info(f'Получили данные: {name}, {category}, {description}, {price}, {quantity}')
            product = Product(name=name, category=category, description=description, price=price, quantity=quantity, image=image, active=active)
            product.save()
            #messages.success(request, f'Товар {name} добавлен')
            return redirect('product_info', product_id=product.id)

    else:
        form = ProductForm()
        message = 'Введите данные товара'
    return render(request, 'add_product.html', {'form': form, 'message': message})

# HW-4 25.04.24
def product_info(request, product_id):
    '''Отображение информации о товаре'''
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'product_info.html', {'product': product, 'title': 'Информация о товаре'})

# HW-4 25.04.24
def category_all(request):
    '''Отображение всех категорий'''
    categories = Product.objects.values('category').distinct()
    category_names = dict(CATEGORY_CHOICES)
    category_list = [category_names[category['category']] for category in categories]
    print(category_list, 'category_list')
    return render(request, 'categories_all.html', {'categories': category_list})


# HW-4 25.04.24
def product_category(request, category):
    '''Отображение товаров по категориям'''
    print(category, 'category')
    category_names_titles = category
    category_names = dict((v, k) for k, v in CATEGORY_CHOICES)
    category = category_names.get(category)
    products = Product.objects.filter(category=category)
    return render(request, 'products_category.html', {'products': products, 'category': category, 'category_names_titles': category_names_titles})

# Запуск сервера: py manage.py runserver