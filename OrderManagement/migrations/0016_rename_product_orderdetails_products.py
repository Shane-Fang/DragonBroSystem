# Generated by Django 4.2 on 2023-12-25 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0015_rename_products_orderdetails_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetails',
            old_name='Product',
            new_name='Products',
        ),
    ]
