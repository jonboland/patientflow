# Generated by Django 3.2.11 on 2022-02-07 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_patient_organisation'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='patient',
            name='appointment_needed',
        ),
        migrations.AddField(
            model_name='patient',
            name='status',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='patients.appointmentstatus'),
        ),
    ]
