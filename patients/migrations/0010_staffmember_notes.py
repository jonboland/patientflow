# Generated by Django 3.2.11 on 2022-02-09 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0009_auto_20220209_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='staffmember',
            name='notes',
            field=models.TextField(blank=True),
        ),
    ]
