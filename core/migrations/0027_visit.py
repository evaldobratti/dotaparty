# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0026_auto_20160603_0010'),
    ]

    operations = [
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('host', models.CharField(max_length=400)),
                ('requested', models.CharField(max_length=400)),
                ('last_visit', models.DateTimeField(auto_now=True)),
                ('count', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
