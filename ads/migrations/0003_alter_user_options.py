# Generated by Django 4.2.1 on 2023-06-06 13:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['username'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
