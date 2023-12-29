# Generated by Django 4.2 on 2023-12-28 13:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0009_transpose_user'),
        ('Product', '0009_alter_branch_inventory_products'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restockdetail',
            name='Branch',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='member.branchs', verbose_name='分店ID'),
        ),
    ]
