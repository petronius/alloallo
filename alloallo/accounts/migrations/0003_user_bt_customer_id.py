# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def data_migration(apps, schema_editor):
    users = apps.get_model("accounts", "User")
    for user in users.objects.all():
        user.bt_customer_id = -1
        user.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bt_customer_id',
            field=models.IntegerField(default=-1),
        ),
        migrations.RunPython(
            data_migration
        )
    ]
