# Generated by Django 3.1.5 on 2021-01-23 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('regioni', '0008_auto_20210123_1156'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='regioniitaliane',
            name='percentuale_tamponi_test_antigenico_rapido_3dma',
        ),
        migrations.RemoveField(
            model_name='regioniitaliane',
            name='percentuale_tamponi_test_antigenico_rapido_7dma',
        ),
        migrations.RemoveField(
            model_name='regioniitaliane',
            name='percentuale_totale_positivi_test_antigenico_rapido_3dma',
        ),
        migrations.RemoveField(
            model_name='regioniitaliane',
            name='percentuale_totale_positivi_test_antigenico_rapido_7dma',
        ),
        migrations.RemoveField(
            model_name='regioniitaliane',
            name='percentuale_totale_positivi_test_molecolare_3dma',
        ),
        migrations.RemoveField(
            model_name='regioniitaliane',
            name='percentuale_totale_positivi_test_molecolare_7dma',
        ),
    ]