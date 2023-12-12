# Generated by Django 4.2 on 2023-12-11 15:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0008_remove_user_address_alter_user_email_and_more'),
        ('Product', '0003_alter_itemimage_imageid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Branch_Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Number', models.IntegerField(verbose_name='總庫存')),
                ('Branch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='member.branchs', verbose_name='店家')),
            ],
            options={
                'verbose_name': '進貨商品管理',
                'verbose_name_plural': '進貨商品管理',
            },
        ),
        migrations.AlterModelOptions(
            name='products',
            options={'verbose_name': '商品管理', 'verbose_name_plural': '商品管理'},
        ),
        migrations.RemoveField(
            model_name='itemimage',
            name='Product_list',
        ),
        migrations.RemoveField(
            model_name='products',
            name='Branch',
        ),
        migrations.RemoveField(
            model_name='products',
            name='ExpiryDate',
        ),
        migrations.RemoveField(
            model_name='products',
            name='Product_list',
        ),
        migrations.AddField(
            model_name='itemimage',
            name='Products',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='Product.products', verbose_name='商品'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='Category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Product.categories', verbose_name='類別'),
        ),
        migrations.AddField(
            model_name='products',
            name='Item_name',
            field=models.CharField(blank=True, max_length=99, null=True, verbose_name='貨品名稱'),
        ),
        migrations.AddField(
            model_name='products',
            name='Price',
            field=models.IntegerField(default=0, verbose_name='建議售價'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='products',
            name='Sh',
            field=models.IntegerField(choices=[(0, '下架'), (1, '上架')], default=1, verbose_name='上/下架'),
        ),
        migrations.AddField(
            model_name='products',
            name='Specification',
            field=models.CharField(default=0, max_length=99, verbose_name='規格'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='products',
            name='Number',
            field=models.IntegerField(verbose_name='庫存'),
        ),
        migrations.DeleteModel(
            name='Products_list',
        ),
        migrations.AddField(
            model_name='branch_inventory',
            name='Products',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Product.products', verbose_name='商品'),
        ),
    ]