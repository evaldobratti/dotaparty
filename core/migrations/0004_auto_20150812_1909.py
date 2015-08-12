# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection


def migrate_abilities_upgrades(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute("""UPDATE core_detailmatchabilityupgrade AU
      SET CABILITY_ID = (SELECT a.ABILITY_ID FROM core_ability A WHERE A.ID = AU.ABILITY_ID )""")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_auto_20150812_1909'),
    ]

    operations = [
        migrations.RunPython(migrate_abilities_upgrades),
    ]
