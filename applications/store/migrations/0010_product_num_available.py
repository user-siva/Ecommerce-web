# Generated by Django 3.1.6 on 2021-02-19 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_productimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='num_available',
            field=models.IntegerField(default=1),
        ),
    ]
