# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='paid', help_text="Whether the user has paid for their account. Unpaid accounts can't use the service."),
        ),
        migrations.AlterField(
            model_name='user',
            name='bt_customer_id',
            field=models.IntegerField(),
        ),
    ]
