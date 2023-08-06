.. image:: https://travis-ci.org/mp0wer/django-yamoney.svg?branch=master
    :target: https://travis-ci.org/mp0wer/django-yamoney

=======
Yamoney
=======

Django приложение для приема денег на кошелек Yandex.Money

Установка
---------

1. Установить::

    pip install django-yamoney

2. Добавить "yamoney" в ваш INSTALLED_APPS::

    INSTALLED_APPS = (
        ...
        'yamoney',
    )

3. Добавить yamoney URLconf в urls.py вашего проекта::

    url(r'^yamoney/', include('yamoney.urls'))

4. Создать форму оплаты с помощью yamoney.forms.paymentform_factory::

    payment_form = paymentform_factory(
        'Оплата участия',  # описание платежа
        2000,               # сумма
        event               # объект модели
    )

5. Слушать yamoney.signals.transaction_success сигнал, где sender - транзакция, related_obj - объект модели.

