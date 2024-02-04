# Generated by Django 4.2.4 on 2024-02-04 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0022_remove_products_import_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='Product.categories', verbose_name='類別'),
        ),
    ]
