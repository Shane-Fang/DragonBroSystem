# Generated by Django 4.2 on 2023-12-21 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('OrderManagement', '0009_alter_orderdetails_product_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orderdetails',
            old_name='Product',
            new_name='Branch_Inventory',
        ),
        migrations.RenameField(
            model_name='shoppingcartdetails',
            old_name='Product',
            new_name='Branch_Inventory',
        ),
    ]
