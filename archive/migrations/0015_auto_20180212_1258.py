# Generated by Django 2.0.1 on 2018-02-12 12:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('archive', '0014_auto_20180212_1212'),
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.TextField()),
                ('output', models.TextField()),
            ],
        ),
        migrations.RemoveField(
            model_name='problem',
            name='grader',
        ),
        migrations.AddField(
            model_name='problem',
            name='Input specification',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='problem',
            name='Output specification',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='problem',
            name='time_limit',
            field=models.IntegerField(default=2),
        ),
        migrations.AddField(
            model_name='example',
            name='problem',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examples', to='archive.Problem'),
        ),
    ]