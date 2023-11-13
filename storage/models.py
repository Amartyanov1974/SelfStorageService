from django.db import models
from django.contrib.auth.models import User


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
                                   max_length=50)
    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'

    def __str__(self):
        return f'{self.user}: {self.address}, {self.phonenumber}'
