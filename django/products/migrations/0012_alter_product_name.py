# Generated by Django 4.1.8 on 2023-05-28 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_merge_20230526_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='name',
            field=models.CharField(max_length=200),
        ),
    ]
