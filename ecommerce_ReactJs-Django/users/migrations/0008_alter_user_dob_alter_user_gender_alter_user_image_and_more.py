# Generated by Django 4.2.5 on 2023-10-31 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_alter_user_age_alter_user_dob_alter_user_gender_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='dob',
            field=models.DateField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(default=0, max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.CharField(default=0, max_length=500),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(default=0, max_length=25),
        ),
    ]