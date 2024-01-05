# Generated by Django 4.2.4 on 2024-01-05 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_remove_products_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restock',
            name='Category',
            field=models.IntegerField(blank=True, choices=[(0, '進貨'), (1, 'BtoB'), (2, 'BtoC')], default=0, null=True, verbose_name='進貨狀態'),
        ),
    ]