# Generated by Django 4.2.4 on 2023-12-03 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_branchs_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='branchs',
            name='address',
            field=models.CharField(default=0, max_length=255, verbose_name='店家地址'),
            preserve_default=False,
        ),
    ]
