# Generated by Django 3.1.2 on 2020-12-09 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('province', '0005_provinceitaliane_ingressi_terapia_intensiva'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='provinceitaliane',
            name='ingressi_terapia_intensiva',
        ),
    ]
