# Generated by Django 5.0.3 on 2024-03-20 05:31

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Batch',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('data', models.JSONField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BatchProfile',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('batch', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='batchProfile', to='analysis.batch')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BatchProfilePayload',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('fullName', models.CharField(blank=True, max_length=255, null=True)),
                ('firstName', models.CharField(blank=True, max_length=255, null=True)),
                ('lastName', models.CharField(blank=True, max_length=255, null=True)),
                ('emailAddress', models.EmailField(blank=True, max_length=254, null=True)),
                ('phone', models.CharField(blank=True, max_length=255, null=True)),
                ('jobTitle', models.CharField(blank=True, max_length=255, null=True)),
                ('hashedEmail', models.CharField(blank=True, max_length=255, null=True)),
                ('lastUpdatedDateAfter', models.DateField(blank=True, null=True)),
                ('validDateAfter', models.DateField(blank=True, null=True)),
                ('companyId', models.CharField(blank=True, max_length=255, null=True)),
                ('companyName', models.CharField(blank=True, max_length=255, null=True)),
                ('contactAccuracyScoreMin', models.IntegerField(blank=True, null=True)),
                ('batchProfile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='batchprofilepayload', to='analysis.batchprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactDetails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('firstName', models.CharField(blank=True, max_length=255, null=True)),
                ('middleName', models.CharField(blank=True, max_length=255, null=True)),
                ('lastName', models.CharField(blank=True, max_length=255, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('hasCanadianEmail', models.BooleanField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('directPhoneDoNotCall', models.BooleanField(blank=True, null=True)),
                ('street', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('region', models.CharField(blank=True, max_length=255, null=True)),
                ('metroArea', models.CharField(blank=True, max_length=255, null=True)),
                ('zipCode', models.CharField(blank=True, max_length=20, null=True)),
                ('state', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('continent', models.CharField(blank=True, max_length=255, null=True)),
                ('personHasMoved', models.BooleanField(blank=True, null=True)),
                ('withinEu', models.BooleanField(blank=True, null=True)),
                ('withinCalifornia', models.BooleanField(blank=True, null=True)),
                ('withinCanada', models.BooleanField(blank=True, null=True)),
                ('validDate', models.DateField(blank=True, null=True)),
                ('lastUpdatedDate', models.CharField(blank=True, max_length=255, null=True)),
                ('noticeProvidedDate', models.DateField(blank=True, null=True)),
                ('salutation', models.CharField(blank=True, max_length=255, null=True)),
                ('suffix', models.CharField(blank=True, max_length=255, null=True)),
                ('jobTitle', models.CharField(blank=True, max_length=255, null=True)),
                ('jobFunction', models.CharField(blank=True, max_length=255, null=True)),
                ('education', models.CharField(blank=True, max_length=255, null=True)),
                ('picture', models.CharField(blank=True, max_length=255, null=True)),
                ('mobilePhoneDoNotCall', models.BooleanField(blank=True, null=True)),
                ('managementLevel', models.CharField(blank=True, max_length=255, null=True)),
                ('contactAccuracyScore', models.IntegerField(blank=True, null=True)),
                ('companyId', models.CharField(blank=True, max_length=255, null=True)),
                ('companyName', models.CharField(blank=True, max_length=255, null=True)),
                ('companyDescriptionList', models.TextField(blank=True, null=True)),
                ('companyPhone', models.CharField(blank=True, max_length=255, null=True)),
                ('companyFax', models.CharField(blank=True, max_length=255, null=True)),
                ('companyStreet', models.CharField(blank=True, max_length=255, null=True)),
                ('companyCity', models.CharField(blank=True, max_length=255, null=True)),
                ('companyState', models.CharField(blank=True, max_length=255, null=True)),
                ('companyZipCode', models.CharField(blank=True, max_length=255, null=True)),
                ('companyCountry', models.CharField(blank=True, max_length=255, null=True)),
                ('companyContinent', models.CharField(blank=True, max_length=255, null=True)),
                ('companyLogo', models.CharField(blank=True, max_length=255, null=True)),
                ('companyDivision', models.CharField(blank=True, max_length=255, null=True)),
                ('companySicCodes', models.CharField(blank=True, max_length=255, null=True)),
                ('companyNaicsCodes', models.CharField(blank=True, max_length=255, null=True)),
                ('companyWebsite', models.CharField(blank=True, max_length=255, null=True)),
                ('companyRevenue', models.CharField(blank=True, max_length=255, null=True)),
                ('companyRevenueNumeric', models.IntegerField(blank=True, null=True)),
                ('companyEmployeeCount', models.CharField(blank=True, max_length=255, null=True)),
                ('companyType', models.CharField(blank=True, max_length=255, null=True)),
                ('companyTicker', models.CharField(blank=True, max_length=255, null=True)),
                ('companyRanking', models.CharField(blank=True, max_length=255, null=True)),
                ('isDefunct', models.BooleanField(blank=True, null=True)),
                ('companyPrimaryIndustry', models.CharField(blank=True, max_length=255, null=True)),
                ('companyRevenueRange', models.CharField(blank=True, max_length=255, null=True)),
                ('companyEmployeeRange', models.CharField(blank=True, max_length=255, null=True)),
                ('locationCompanyId', models.CharField(blank=True, max_length=255, null=True)),
                ('positionStartDate', models.CharField(blank=True, max_length=255, null=True)),
                ('yearsOfExperience', models.IntegerField(blank=True, null=True)),
                ('data_source', models.CharField(choices=[('linkedin_package', 'linkedin_package'), ('linkedin_selenium', 'linkedin_selenium')], max_length=20)),
                ('batchProfilePayload', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactDetails', to='analysis.batchprofilepayload')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactCompanySocialMediaUrls',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('facebook', models.CharField(blank=True, max_length=255, null=True)),
                ('linkedIn', models.CharField(blank=True, max_length=255, null=True)),
                ('contactDetails', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactCompanySocialMediaUrls', to='analysis.contactdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactCompanyIndustries',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('contactDetails', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactCompanyIndustries', to='analysis.contactdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactEmploymentHistory',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('companyName', models.CharField(blank=True, max_length=255, null=True)),
                ('jobTitle', models.CharField(blank=True, max_length=255, null=True)),
                ('startDate', models.CharField(blank=True, max_length=255, null=True)),
                ('endDate', models.CharField(blank=True, max_length=255, null=True)),
                ('contactDetails', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactEmploymentHistory', to='analysis.contactdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactExternalUrls',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('linkedIn', models.CharField(blank=True, max_length=255, null=True)),
                ('twitter', models.CharField(blank=True, max_length=255, null=True)),
                ('contactDetails', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactExternalUrls', to='analysis.contactdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactHashedEmails',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('mail', models.EmailField(max_length=254)),
                ('contactDetails', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactHashedEmails', to='analysis.contactdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactSourceSystem',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('contactDetails', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactSourceSystem', to='analysis.contactdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ContactTechSkills',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('skill', models.CharField(blank=True, max_length=255, null=True)),
                ('contactDetails', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='contactTechSkills', to='analysis.contactdetails')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('migrationId', models.CharField(max_length=255)),
                ('tableName', models.CharField(max_length=255)),
                ('recordId', models.CharField(max_length=255)),
                ('status', models.BooleanField(default=0)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
            ],
            options={
                'unique_together': {('migrationId', 'tableName', 'recordId')},
            },
        ),
        migrations.AddField(
            model_name='batchprofile',
            name='profile',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='batchProfile', to='analysis.profile'),
        ),
    ]
