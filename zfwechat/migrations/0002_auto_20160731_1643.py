# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('zfwechat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studentNo', models.CharField(max_length=11)),
                ('studentPsw', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=55)),
                ('markNum', models.IntegerField(max_length=11)),
            ],
        ),
        migrations.DeleteModel(
            name='Person',
        ),
    ]
