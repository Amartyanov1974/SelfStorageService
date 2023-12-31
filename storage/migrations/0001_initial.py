# Generated by Django 4.0 on 2023-11-19 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0013_alter_user_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25, verbose_name='Обозначение')),
                ('length', models.FloatField(verbose_name='Длина')),
                ('width', models.FloatField(verbose_name='Ширина')),
                ('height', models.FloatField(verbose_name='Высота')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('is_occupied', models.BooleanField(default=False, verbose_name='Занят')),
            ],
            options={
                'verbose_name': 'Бокс',
                'verbose_name_plural': 'Боксы',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='client', serialize=False, to='auth.user', verbose_name='Клиент')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Адрес клиента')),
                ('phonenumber', models.CharField(blank=True, max_length=50, null=True, verbose_name='Номер телефона')),
                ('need_call', models.BooleanField(default=False, verbose_name='Нужно перезвонить')),
                ('need_invoice', models.BooleanField(default=False, verbose_name='Нужен счет')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numer', models.IntegerField(verbose_name='Номер склада')),
                ('city', models.CharField(blank=True, max_length=25, verbose_name='Город склада')),
                ('address', models.TextField(verbose_name='Адрес склада')),
                ('feature', models.CharField(max_length=25, verbose_name='Особенность склада')),
                ('image', models.ImageField(blank=True, upload_to='', verbose_name='Фото склада')),
            ],
            options={
                'verbose_name': 'Склад',
                'verbose_name_plural': 'Склады',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('paid_with', models.DateField(blank=True, null=True, verbose_name='Оплачено c')),
                ('price', models.IntegerField(blank=True, null=True, verbose_name='Стоимость')),
                ('size', models.CharField(blank=True, max_length=50, null=True, verbose_name='Размер')),
                ('paid', models.BooleanField(default=False, verbose_name='Оплачен')),
                ('box', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='storage.box', verbose_name='Бокс')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='orders', to='storage.client', verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.AddField(
            model_name='box',
            name='storage',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='boxes', to='storage.storage', verbose_name='Склад'),
        ),
    ]
