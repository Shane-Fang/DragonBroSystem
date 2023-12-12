# Generated by Django 4.2 on 2023-12-11 15:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('member', '0008_remove_user_address_alter_user_email_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Product', '0003_alter_itemimage_imageid'),
        ('OrderManagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Restock',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.IntegerField(blank=True, choices=[(0, '代處理'), (1, '已處理')], default=1, null=True, verbose_name='運送狀態')),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('Type', models.IntegerField(blank=True, choices=[(0, '代處理'), (1, '已處理')], default=1, null=True, verbose_name='運送狀態')),
                ('object_id', models.PositiveIntegerField()),
                ('Branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='member.branchs', verbose_name='分店ID')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='後台操作的員工')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
        ),
        migrations.CreateModel(
            name='RestockDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ExpiryDate', models.DateField(verbose_name='有效日期')),
                ('Number', models.IntegerField(verbose_name='數量')),
                ('Remain', models.IntegerField(verbose_name='剩餘數量')),
                ('Branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='member.branchs', verbose_name='分店ID')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.products', verbose_name='商品')),
                ('Restock', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='OrderManagement.restock', verbose_name='交易')),
            ],
        ),
        migrations.AddField(
            model_name='orders',
            name='Address',
            field=models.CharField(default=0, max_length=255, verbose_name='地址'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='RestockDetail_relation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.IntegerField(verbose_name='數量')),
                ('InID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='InID', to='OrderManagement.restockdetail', verbose_name='交易')),
                ('OutID', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='OutID', to='OrderManagement.restockdetail', verbose_name='交易')),
            ],
        ),
        migrations.CreateModel(
            name='OrderLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('Delivery_state', models.IntegerField(blank=True, choices=[(0, '代處理'), (1, '已處理')], default=1, null=True, verbose_name='運送狀態')),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='OrderManagement.orders', verbose_name='訂單')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, verbose_name='後台操作的員工')),
            ],
        ),
    ]