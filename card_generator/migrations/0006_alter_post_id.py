# Generated by Django 3.2.8 on 2021-11-18 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card_generator', '0005_auto_20211117_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
