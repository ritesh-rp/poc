# Generated by Django 5.0.3 on 2024-04-01 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("analysis", "0002_remove_profile_status_batchprofilepayload_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="batchprofilepayload",
            name="status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Success", "Success"),
                    ("Failed", "Failed"),
                ],
                default="Pending",
                max_length=50,
            ),
        ),
    ]
