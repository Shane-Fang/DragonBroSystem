# Generated by Django 4.2.4 on 2023-12-03 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0002_products_branch'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemimage',
            name='ImageID',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='圖片id'),
        ),
    ]
