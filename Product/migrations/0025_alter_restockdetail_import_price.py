# Generated by Django 4.2.4 on 2024-02-04 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0024_alter_itemimage_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restockdetail',
            name='Import_price',
            field=models.IntegerField(blank=True, null=True, verbose_name='成本價'),
        ),
    ]