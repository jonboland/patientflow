# Generated by Django 3.2.11 on 2022-02-01 16:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0003_auto_20220201_1137'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='organisation',
            field=models.ForeignKey(default=6, on_delete=django.db.models.deletion.CASCADE, to='patients.userprofile'),
            preserve_default=False,
        ),
    ]
