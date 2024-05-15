Задание

Измените модель продукта, добавьте поле для хранения фотографии продукта.

Создайте форму, которая позволит сохранять фото.

Сделано:
<br> Добавить пользователя через форму с фотографией, проверка на уникальность email в БД
<br> Добавить товар через форму с фотографией, проверка на уникальность названия в БД
<br> Отображение списка категорий товара и самих товаров в нутри своей категори


<br> Модели: 
<br> class Product(models.Model)
<br> class ProductImage(models.Model)
<br> class Client(models.Model): + фото

<br> Представления:
<br> def add_user(request) '''Добавление нового пользователя'''
<br> def add_product(request) '''Добавление нового товара'''
<br> def product_info(request, product_id) '''Отображение информации о товаре'''
<br> def category_all(request) '''Отображение всех категорий'''
<br> def product_category(request, category) '''Отображение товаров по категориям'''

<br> Формы:
<br> https://github.com/Teimur-KZ/HW_25-04-24/blob/master/myapp/user_forms.py
<br> https://github.com/Teimur-KZ/HW_25-04-24/blob/master/myapp/product_forms.py
