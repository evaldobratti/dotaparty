# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection

def migrate_player_heroes(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute("""UPDATE core_detailmatchplayer MP
      SET CHERO_ID = (SELECT H.HERO_ID FROM core_hero H WHERE H.ID = MP.HERO_ID )""")

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20150812_1909'),
    ]

    operations = [
        migrations.RunPython(migrate_player_heroes),
    ]
