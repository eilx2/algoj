# Generated by Django 2.0.1 on 2018-02-21 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0016_auto_20180212_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='problem',
            name='author',
            field=models.CharField(default='', max_length=40),
        ),
    ]