# Generated by Django 4.2.4 on 2024-01-05 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0012_remove_products_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restockdetail',
            name='Restock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Product.restock', verbose_name='交易'),
        ),
    ]