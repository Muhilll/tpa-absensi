# Generated by Django 5.1.5 on 2025-02-13 22:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admintpa', '0003_absensi_batas_alter_absensi_tanggal'),
    ]

    operations = [
        migrations.AddField(
            model_name='kehadiran',
            name='tanggal',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
