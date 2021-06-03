# Generated by Django 3.2.3 on 2021-06-02 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('max_way', '0002_auto_20210527_1958'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='products',
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='product',
            name='foods',
            field=models.ManyToManyField(blank=True, related_name='_max_way_product_foods_+', to='max_way.Product'),
        ),
        migrations.AlterField(
            model_name='user',
            name='price_type',
            field=models.PositiveIntegerField(default=0),
        ),
    ]