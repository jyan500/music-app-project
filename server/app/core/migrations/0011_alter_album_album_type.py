# Generated by Django 3.2.23 on 2024-02-08 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20240201_0045'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='album_type',
            field=models.CharField(choices=[('ALBUM', 'Album'), ('SINGLE', 'Single'), ('COMPILATION', 'Compilation')], default='COMPILATION', max_length=50),
        ),
    ]
