# Generated by Django 4.1.2 on 2022-11-13 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_orderitem_order'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='orderd',
            new_name='ordered',
        ),
        migrations.RenameField(
            model_name='orderitem',
            old_name='orderd',
            new_name='ordered',
        ),
    ]
