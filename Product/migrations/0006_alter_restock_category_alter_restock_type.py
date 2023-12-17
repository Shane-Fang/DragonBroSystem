# Generated by Django 4.2.4 on 2023-12-16 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0005_restock_restockdetail_alter_branch_inventory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restock',
            name='Category',
            field=models.IntegerField(blank=True, choices=[(0, '進貨'), (1, 'BtoB'), (2, 'BtoC')], default=1, null=True, verbose_name='運送狀態'),
        ),
        migrations.AlterField(
            model_name='restock',
            name='Type',
            field=models.IntegerField(blank=True, choices=[(0, '進貨'), (1, '出貨')], default=1, null=True, verbose_name='運送狀態'),
        ),
    ]
