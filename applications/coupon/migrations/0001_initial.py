# Generated by Django 3.1.6 on 2021-02-08 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('value', models.IntegerField()),
                ('active', models.BooleanField(default=True)),
                ('num_available', models.IntegerField(default=1)),
                ('num_used', models.IntegerField(default=0)),
            ],
        ),
    ]
