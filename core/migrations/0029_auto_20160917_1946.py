# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_proxy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proxy',
            name='last_success',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
