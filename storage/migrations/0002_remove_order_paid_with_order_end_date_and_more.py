# Generated by Django 4.0 on 2023-11-19 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storage', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='paid_with',
        ),
        migrations.AddField(
            model_name='order',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Окончание хранения'),
        ),
        migrations.AddField(
            model_name='order',
            name='send_message',
            field=models.BooleanField(default=False, verbose_name='Отправить уведомление'),
        ),
        migrations.AddField(
            model_name='order',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Начало хранения'),
        ),
    ]
