from datetime import datetime, timedelta, timezone

import requests
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Max, Min

from selfstorage.settings import BITLY_TOKEN


class Client(models.Model):
    user = models.OneToOneField(User,
                                verbose_name='Клиент',
                                on_delete=models.CASCADE,
                                primary_key=True,
                                related_name='client')
    address = models.TextField(verbose_name='Адрес клиента',
                               blank=True,
                               null=True)
    phonenumber = models.CharField(verbose_name='Номер телефона',
                                   max_length=50,
                                   null=True,
                                   blank=True)
    need_call = models.BooleanField(verbose_name='Нужно перезвонить',
                                    default=False)
    need_invoice = models.BooleanField(verbose_name='Нужен счет',
                                    default=False)

    @property
    def user_email(self):
        return self.user.email

    @property
    def user_name(self):
        return self.user.first_name

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.user_name}: {self.address}, {self.phonenumber}'


class StorageQuerySet(models.QuerySet):
    def get_boxes(self):
        for storage in self:
            storage.count_of_free_boxes = storage.boxes.filter(is_occupied=False).count()
            storage.count_boxes = storage.boxes.count()
            min_price = storage.boxes.aggregate(Min('price'))
            storage.min_price = min_price['price__min']
            max_height = storage.boxes.aggregate(Max('height'))
            storage.max_height = max_height['height__max']
        return self


class Storage(models.Model):
    numer = models.IntegerField(verbose_name='Номер склада')
    city = models.CharField(max_length=25, verbose_name='Город склада', blank=True)
    address = models.TextField(verbose_name='Адрес склада')
    feature = models.CharField(max_length=25, verbose_name='Особенность склада')
    image = models.ImageField(verbose_name='Фото склада', blank=True)

    objects = StorageQuerySet.as_manager()

    def __str__(self):
        return f'{self.numer} {self.address}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Box(models.Model):
    name = models.CharField(max_length=25, verbose_name='Обозначение')
    storage = models.ForeignKey(Storage, verbose_name='Склад',
                                on_delete=models.CASCADE,
                                related_name='boxes')
    length = models.FloatField(verbose_name='Длина')
    width = models.FloatField(verbose_name='Ширина')
    height = models.FloatField(verbose_name='Высота')
    price = models.IntegerField(verbose_name='Цена')
    is_occupied = models.BooleanField(verbose_name='Занят', default=False)

    def __str__(self):
        return f'{self.name}({self.length}x{self.width}x{self.height} м)'

    class Meta:
        verbose_name = 'Бокс'
        verbose_name_plural = 'Боксы'


class Order(models.Model):
    client = models.ForeignKey(Client,
                               on_delete=models.CASCADE,
                               related_name='orders',
                               verbose_name='Клиент')
    created_at = models.DateTimeField(verbose_name='Создано',
                                      auto_now_add=True)
    box = models.ForeignKey(Box,
                            on_delete=models.SET_NULL,
                            related_name='orders',
                            verbose_name='Бокс',
                            null=True,
                            blank=True,
                            default=None)
    start_date = models.DateField(verbose_name="Начало хранения",
                                 null=True,
                                 blank=True)
    end_date = models.DateField(verbose_name="Окончание хранения",
                                 null=True,
                                 blank=True)

    price = models.IntegerField(verbose_name='Стоимость',
                                null=True,
                                blank=True)

    size = models.CharField(max_length=50,
                            verbose_name='Размер',
                            null=True,
                            blank=True)
    paid = models.BooleanField(verbose_name='Оплачен',
                                    default=False)

    send_message = models.BooleanField(verbose_name='Отправить уведомление',
                                    default=False)

    @property
    def days_left(self):
        if self.end_date:
            delta = self.end_date - datetime.now().date()
            days = delta.days
            if days < 5:
                self.send_message = True
        else:
            days = None
        return days

    @property
    def storage(self):
        try:
            storage = self.box.storage
        except:
            storage = None
        return storage

    def __str__(self):
        return f'#{self.pk} {self.client} {self.storage} {self.box}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class LinkStatistics(models.Model):
    def save(self, *args, **kwargs):
        def shorten_link(token, link):
            url = 'https://api-ssl.bitly.com/v4/bitlinks'
            headers = {
                "Authorization": f"Bearer {token}"
            }
            body = {
                "long_url": link
            }
            response = requests.post(url, headers=headers, json=body)
            response.raise_for_status()
            bitlink = response.json()['link']
            return bitlink

        if self.link:
            self.bitlink = shorten_link(BITLY_TOKEN, self.link)
        super().save(*args, **kwargs)

    link = models.CharField(max_length=200, verbose_name='Простая ссылка', null=True, blank=True)
    bitlink = models.CharField(max_length=200, verbose_name='Bitly ссылка', null=True, blank=True)
    transitions = models.IntegerField(verbose_name='Количество переходов по ссылке', null=True, blank=True, default=0)