# Generated by Django 3.2.3 on 2021-06-02 11:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('max_way', '0004_alter_category_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='order',
            table='order',
        ),
        migrations.AlterModelTable(
            name='product',
            table='product',
        ),
        migrations.AlterModelTable(
            name='user',
            table='user',
        ),
    ]
