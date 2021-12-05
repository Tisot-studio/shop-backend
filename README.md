API интернет магазина.

Сервис готов к работе, осталось только 
1. Клонировать репозиторий и зайти в него  
git clone https://github.com/Tisot-studio/shop-backend.git
cd shop-backend

2. Создать виртуальное окружение и запустить его, например:  
py -m venv testenv  
testenv\Scripts\activate 

3. Установить все необходимые пакеты:  
pip install -r requirements.txt

4. В файле settings.py настроить отправку электронной почты:

    EMAIL_HOST_USER = 'почта_откуда_будут_отправляться_письма@mail.com'
    EMAIL_HOST_PASSWORD = 'пароль_к_почте'

5. Запустить сервер  
py manage.py runserver

Можно создавать запросы через Postman! :)

================End Points================================

1. Товары

Получить список товаров магазина 
    GET http://localhost:8000/api/products


Получить товар по id 
    GET http://localhost:8000/api/products/1

2. Пользователь

Что бы совершать какие либо действия в магазине, нужно зарегистрировать пользователя:
Для аутентификации пользователя испоьзуется библиотека Djoser и JWT.
    
    Headers
    Content-Type    application/json

    Body

    {   
        "name": "test",
        "email": "ваш_емейл@gmail.com",
        "password": "ваш_пароль",
        "re_password": "ваш_пароль"
    }

    Отправляем все это на http://127.0.0.1:8000/auth/users/ POST

=====================================================

На почту придет письмо с токеном. Активируем аккаунт.
    Пример: http://127.0.0.1:8000/activate/MTk/ax3m8b-66cc08507db8d591dd1e758d52cc59a8

    Берем из этого токена следующие части:

    Headers
    Content-Type    application/json

    Body
    {
        "uid": "MTk",
        "token": "ax3m8b-66cc08507db8d591dd1e758d52cc59a8"
    }

    И отправляем на http://127.0.0.1:8000/auth/users/activation/ POST

    Придет письмо с подтверждением активации.

=====================================================

Теперь можно получить JWT для дальнейших действий в магазине (Login):

    Headers
    Content-Type    application/json

    Body
    {
        "email": "ваш_емейл@gmail.com",
        "password": "ваш_пароль"
    }

    Отправляем на 
    POST http://127.0.0.1:8000/auth/jwt/create/ 

    В ответ получаем токен access.

=====================================================

Загрузить информацию о пользователе:

    Headers
    Content-Type    application/json
    Authorization   JWT ваш_access_токен

    GET http://127.0.0.1:8000/api/users/profile

=====================================================

Обновить информацию о пользователе:
    
    Headers
    Content-Type    application/json
    Authorization   JWT ваш_access_токен

    Body
    {
    "name": "Mulan",
    "email": "",
    "password": ""
    }

    Обновить можно имя, почту и пароль

    PUT http://127.0.0.1:8000/api/users/profile/update

=====================================================

Сброс пароля

    Headers
    Content-Type    application/json
    Authorization   JWT ваш_access_токен

    Body
    {
    "email": "ваша_почта",
    }


    POST http://127.0.0.1:8000/auth/users/reset_password/

=====================================================

Восстанавление пароля:

    Придет письмо на указанный электронный адрес с токеном. Из токена берем части после confirm/

    Например:
    http://127.0.0.1:8000/email/reset/confirm/MTk/ax6y2w-558bb51051ef07ad03a75e64448dd5ee

    Headers
    Content-Type    application/json
    Authorization   JWT ваш_access_токен

    Body
    {
        "uid": "MTk",
        "token": "ax6y2w-558bb51051ef07ad03a75e64448dd5ee",
        "new_password" : "ваш_новый_пароль",
        "re_new_password" : "ваш_новый_пароль"
    }
И отправляем на

POST http://127.0.0.1:8000/auth/users/reset_password_confirm/

Придет письмо с подтверждением, что пароль был восстановлен.


4. Заказы

Создать заказ:

    Headers
    Content-Type    application/json
    Authorization   JWT ваш_access_токен

    Body
    {
        "paymentMethod": "PayPal",
        "taxPrice": "0",
        "shippingPrice" : "1000",
        "orderPrice" : "2000",
        "orderItems": [
        {
            "_id": 1,
            "title": "Prod_1",
            "price": "400.00",
            "imageCover": "http://127.0.0.1:8000/images/24h-anti-ageing-cream_960x_73Ipbt6.jpg",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec efficitur, leo at faucibus euismod, metus felis blandit neque, in tincidunt eros enim sit amet tellus.",
            "available": 50,
            "quantity" : "2"
        },
        {
            "_id": 2,
            "title": "Prod_2",
            "price": "500.00",
            "imageCover": "http://127.0.0.1:8000/images/balancing-foam-cleanser_960x_divLfQu.jpg",
            "description": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec efficitur, leo at faucibus euismod, metus felis blandit neque, in tincidunt eros enim sit amet tellus.",
            "available": 98,
            "quantity" : "2"
        }
        ],

        "city" : "Moscow",
        "street" : "Some street",
        "house" : "45",
        "postalCode" : "123456",
        "phone": "+7-999-999-99-99"
    }

    POST http://127.0.0.1:8000/api/orders/add

=====================================================

После создания заказа, можно посмотреть его номер:
    
    Headers
    Authorization   JWT ваш_access_токен

    GET http://127.0.0.1:8000/api/my_orders

    Получить информацию по конкретному заказу (через id):

    Headers
    Authorization   JWT ваш_access_токен

    GET http://127.0.0.1:8000/api/order/id_нужного_заказа
