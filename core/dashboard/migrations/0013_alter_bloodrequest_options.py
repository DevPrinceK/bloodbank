# Generated by Django 4.1.7 on 2023-04-28 08:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("dashboard", "0012_alter_patientprofile_blood_type"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="bloodrequest",
            options={
                "permissions": [
                    ("change_request_status", "Can change blood request status")
                ]
            },
        ),
    ]