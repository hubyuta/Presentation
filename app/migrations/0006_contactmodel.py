# Generated by Django 4.1.3 on 2023-01-01 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_payment_order_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='氏名')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('subject', models.CharField(max_length=30, verbose_name='件名')),
                ('message', models.CharField(max_length=500, verbose_name='メッセージ')),
                ('timestamp', models.DateTimeField(auto_now_add=True, verbose_name='投稿日時')),
            ],
        ),
    ]
