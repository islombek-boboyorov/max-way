# Generated by Django 3.2.3 on 2021-06-23 07:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('max_way', '0010_alter_bot_user_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bot_user',
            name='chat_id',
            field=models.IntegerField(default=0, null=True),
        ),
    ]