# Generated by Django 4.2.4 on 2024-02-02 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0016_alter_restockdetail_expirydate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch_inventory',
            name='Number',
            field=models.IntegerField(default=0, verbose_name='總庫存'),
        ),
    ]
