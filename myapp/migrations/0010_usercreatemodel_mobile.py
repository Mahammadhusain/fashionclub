# Generated by Django 3.0.3 on 2021-03-18 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_auto_20210318_1013'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercreatemodel',
            name='mobile',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
