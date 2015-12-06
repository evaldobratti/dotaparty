# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together=set([('creator', 'reported', 'due_to_match')]),
        ),
    ]
