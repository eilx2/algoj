# Generated by Django 2.0.1 on 2018-02-12 13:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0015_auto_20180212_1258'),
    ]

    operations = [
        migrations.RenameField(
            model_name='problem',
            old_name='Input specification',
            new_name='input_spec',
        ),
        migrations.RenameField(
            model_name='problem',
            old_name='Output specification',
            new_name='output_spec',
        ),
    ]