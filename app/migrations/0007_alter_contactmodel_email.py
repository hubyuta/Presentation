# Generated by Django 4.1.3 on 2023-01-02 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_contactmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactmodel',
            name='email',
            field=models.EmailField(max_length=254, verbose_name='メールアドレス'),
        ),
    ]
