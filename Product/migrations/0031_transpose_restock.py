# Generated by Django 4.2.4 on 2024-02-05 16:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Product', '0030_transpose'),
    ]

    operations = [
        migrations.AddField(
            model_name='transpose',
            name='Restock',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.restock', verbose_name='進出貨'),
        ),
    ]
