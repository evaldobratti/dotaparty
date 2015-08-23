# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from core import parameters
def create_parameters(apps, schema_editor):
    Parameter = apps.get_model("core", "Parameter")

    Parameter.objects.create(name=parameters.LAST_MATCH_ID_SKILL_UNDEFINED, value=None)

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_detailmatch_skill'),
    ]

    operations = [
        migrations.RunPython(create_parameters),
    ]
