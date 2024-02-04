# Generated by Django 4.2.4 on 2024-02-04 16:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('OrderManagement', '0018_alter_orderdetails_delivery_state'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderlog',
            name='Delivery_state',
            field=models.IntegerField(blank=True, choices=[(0, '未處理'), (1, '待出貨'), (2, '待付款'), (3, '代收貨'), (4, '完成訂單'), (5, '退貨'), (6, '退款')], default=1, null=True, verbose_name='運送狀態'),
        ),
        migrations.AlterField(
            model_name='orderlog',
            name='User',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='下單者'),
        ),
        migrations.CreateModel(
            name='OrderDetailsLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('Delivery_state', models.IntegerField(blank=True, choices=[(0, '未處理'), (1, '待出貨'), (2, '待付款'), (3, '代收貨'), (4, '完成訂單'), (5, '退貨'), (6, '退款')], default=1, null=True, verbose_name='運送狀態')),
                ('OrderDetails', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='OrderManagement.orderdetails', verbose_name='訂單')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='下單者')),
            ],
            options={
                'verbose_name': '訂單明細紀錄',
                'verbose_name_plural': '訂單明細紀錄',
            },
        ),
    ]