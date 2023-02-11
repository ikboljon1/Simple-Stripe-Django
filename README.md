# Setting up Stripe Checkout with Django
## Django Stripe.

Тестовое задание для одной из компаний. Простой магазин Django с Stripe. Основная цель состоит в том, чтобы иметь конечную точку /item/<item_id>, которая будет возвращать HTML с информацией об элементе (из базы данных сервера) и кнопкой покупки, который выберет другой маршрут (API) (/buy/<item_id>), который вернет идентификатор сеанса Stripe, который используется для перенаправления пользователя на экран оплаты (фактически, сам Stripe).

## Хотите использовать этот проект?


1. Создайте и активируйте виртуальную среду:

     ``sh
     $ python3 -m venv venv && source venv/bin/activate
     ```

1. Установите требования:

     ``sh
     (venv)$ pip install -r requirements.txt
     ```

1. Примените миграции:

     ``sh
     (venv)$ python manage.py migrate
     ```

1. Добавьте тестовый секрет Stripe и тестовые публикуемые ключи в файл *settings.py*:

     ```Python
        STRIPE_PUBLISHABLE_KEY = '<your test publishable key here>'
        STRIPE_SECRET_KEY = '<your test secret key here>'
     ```

1. Если вы планируете подтверждать платежи с помощью веб-перехватчиков, вам также необходимо добавить секрет конечной точки веб-перехватчика в файл *settings.py*:

     ```Python
     STRIPE_ENDPOINT_SECRET = '<your endpoint secret here>'
     ```

1. Запускаем сервер:

     ``sh
     (venv)$ сервер запуска python manage.py
     ```