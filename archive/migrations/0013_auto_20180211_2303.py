# Generated by Django 2.0.1 on 2018-02-11 23:03

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0012_auto_20180211_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='statement',
            field=tinymce.models.HTMLField(),
        ),
    ]