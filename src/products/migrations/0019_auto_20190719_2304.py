# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-07-19 23:04
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_auto_20190719_2257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(default='img/default.png', upload_to=products.models.upload_image_path),
        ),
    ]