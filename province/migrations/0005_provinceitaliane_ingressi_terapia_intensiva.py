# Generated by Django 3.1.2 on 2020-12-09 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('province', '0004_auto_20201129_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='provinceitaliane',
            name='ingressi_terapia_intensiva',
            field=models.IntegerField(default=0),
        ),
    ]
