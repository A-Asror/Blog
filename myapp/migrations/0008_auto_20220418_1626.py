# Generated by Django 3.2 on 2022-04-18 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_auto_20220415_1328'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='plays_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='videopost',
            name='plays_count',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
