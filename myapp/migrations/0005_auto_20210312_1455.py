# Generated by Django 3.0.3 on 2021-03-12 14:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_remove_categorymodel_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='categorymodel',
            name='description',
        ),
        migrations.RemoveField(
            model_name='categorymodel',
            name='price',
        ),
    ]
