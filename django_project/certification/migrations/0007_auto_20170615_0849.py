# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certification', '0006_auto_20170615_0807'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='attendee',
            unique_together=set([('firstname', 'surname', 'email', 'certifying_organisation')]),
        ),
        migrations.AlterUniqueTogether(
            name='certificate',
            unique_together=set([('course', 'attendee')]),
        ),
    ]
