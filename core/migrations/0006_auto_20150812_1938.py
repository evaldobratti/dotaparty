# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations, connection

def migrate_owner_items(apps, schema_editor):
    cursor = connection.cursor()
    cursor.execute("""UPDATE core_detailmatchowneritem OI
      SET citem_id = (SELECT i.item_id FROM core_item i WHERE i.ID = OI.ITEM_ID )""")


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20150812_1934'),
    ]

    operations = [
        migrations.RunPython(migrate_owner_items),
    ]
