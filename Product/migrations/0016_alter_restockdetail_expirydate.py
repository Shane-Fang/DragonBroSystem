# Generated by Django 4.2 on 2024-02-01 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0015_alter_products_specification'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restockdetail',
            name='ExpiryDate',
            field=models.DateField(blank=True, null=True, verbose_name='有效日期'),
        ),
    ]
