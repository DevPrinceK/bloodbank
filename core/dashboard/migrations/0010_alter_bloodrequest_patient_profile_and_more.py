# Generated by Django 4.1.7 on 2023-04-23 19:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0009_alter_donation_date_time_donated"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bloodrequest",
            name="patient_profile",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="dashboard.patientprofile",
            ),
        ),
        migrations.AlterField(
            model_name="bloodrequest",
            name="status",
            field=models.CharField(default="PENDING", max_length=20),
        ),
    ]
