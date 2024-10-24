from django.db import models
import uuid 


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)

    class Meta:
        abstract = True


class Batch(BaseModel):
    data = models.JSONField()


class Profile(models.Model):
    uuid = models.UUIDField(default = uuid.uuid4, primary_key=True)
    migrationId = models.CharField(max_length=255, null=False , blank=False)
    tableName = models.CharField(max_length=255, null=False , blank=False)
    recordId = models.CharField(max_length=255, null=False , blank=False)
    created_on = models.DateTimeField(auto_now_add = True)
    updated_on = models.DateTimeField(auto_now = True)
    class Meta:
        unique_together = ('migrationId', 'tableName', 'recordId')

class BatchProfile(BaseModel):
    batch = models.ForeignKey(Batch,on_delete=models.PROTECT, related_name="batchProfile")
    profile = models.ForeignKey(Profile,on_delete=models.PROTECT, related_name="batchProfile")


StatusChoices = (
    ("Pending", "Pending"),
    ("completed", "completed"),
    ("Failed", "Failed"),
)

class BatchProfilePayload(BaseModel):
    fullName = models.CharField(max_length=255, null=True , blank=True)
    firstName = models.CharField(max_length=255, null=True , blank=True)
    lastName = models.CharField(max_length=255, null=True , blank=True)
    emailAddress = models.EmailField(null=True , blank=True)
    phone = models.CharField(max_length=255, null=True , blank=True)
    jobTitle = models.CharField(max_length=255, null=True , blank=True)
    hashedEmail = models.CharField(max_length=255, null=True , blank=True)
    lastUpdatedDateAfter = models.DateField(null=True , blank=True)
    validDateAfter = models.DateField(null=True , blank=True)
    companyId = models.CharField(max_length=255, null=True , blank=True)
    companyName = models.CharField(max_length=255, null=True , blank=True)
    contactAccuracyScoreMin = models.IntegerField(null=True , blank=True)
    batchProfile = models.ForeignKey(BatchProfile,on_delete=models.PROTECT, related_name="batchprofilepayload")
    status = models.CharField(max_length=50, choices= StatusChoices, default="Pending")
    


class ContactDetails(BaseModel):
    batchProfilePayload = models.ForeignKey(BatchProfilePayload,on_delete=models.PROTECT, related_name="contactDetails")
    firstName = models.CharField(max_length=255, null=True , blank=True)
    middleName = models.CharField(max_length=255, null=True , blank=True)
    lastName = models.CharField(max_length=255, null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    hasCanadianEmail = models.BooleanField(null=True , blank=True)
    phone = models.CharField(max_length=20, null=True , blank=True)
    directPhoneDoNotCall = models.BooleanField(null=True , blank=True)
    street = models.CharField(max_length=255, null=True , blank=True)
    city = models.CharField(max_length=255, null=True , blank=True)
    region = models.CharField(max_length=255, null=True , blank=True)
    metroArea = models.CharField(max_length=255, null=True , blank=True)
    zipCode = models.CharField(max_length=20, null=True , blank=True)
    state = models.CharField(max_length=255, null=True , blank=True)
    country = models.CharField(max_length=255, null=True , blank=True)
    continent = models.CharField(max_length=255, null=True , blank=True)
    personHasMoved = models.BooleanField( null=True , blank=True)
    withinEu = models.BooleanField(null=True , blank=True)
    withinCalifornia = models.BooleanField(null=True , blank=True)
    withinCanada = models.BooleanField(null=True , blank=True)
    validDate = models.DateField(null=True , blank=True)
    lastUpdatedDate = models.CharField(max_length=255,null=True , blank=True)
    noticeProvidedDate = models.DateField(null=True , blank=True)
    salutation = models.CharField(max_length=255, null=True , blank=True)
    suffix = models.CharField(max_length=255, null=True , blank=True)
    jobTitle = models.CharField(max_length=255, null=True , blank=True)
    jobFunction = models.CharField(max_length=255, null=True , blank=True)
    education = models.CharField(max_length=255, null=True , blank=True)
    picture = models.CharField(max_length=255, null=True , blank=True)
    mobilePhoneDoNotCall = models.BooleanField(null=True , blank=True)
    managementLevel = models.CharField(max_length=255, null=True , blank=True)
    contactAccuracyScore = models.IntegerField(null=True , blank=True)
    companyId = models.CharField(max_length=255, null=True , blank=True)
    companyName = models.CharField(max_length=255, null=True , blank=True)
    companyDescriptionList = models.TextField(null=True , blank=True)
    companyPhone = models.CharField(max_length=255, null=True , blank=True)
    companyFax = models.CharField(max_length=255, null=True , blank=True)
    companyStreet = models.CharField(max_length=255, null=True , blank=True)
    companyCity = models.CharField(max_length=255, null=True , blank=True)
    companyState = models.CharField(max_length=255, null=True , blank=True)
    companyZipCode = models.CharField(max_length=255, null=True , blank=True)
    companyCountry = models.CharField(max_length=255, null=True , blank=True)
    companyContinent = models.CharField(max_length=255, null=True , blank=True)
    companyLogo = models.CharField(max_length=255, null=True , blank=True)
    companyDivision = models.CharField(max_length=255, null=True , blank=True)
    companySicCodes = models.CharField(max_length=255, null=True , blank=True)
    companyNaicsCodes = models.CharField(max_length=255, null=True , blank=True)
    companyWebsite = models.CharField(max_length=255, null=True , blank=True)
    companyRevenue = models.CharField(max_length=255, null=True , blank=True)
    companyRevenueNumeric = models.IntegerField(null=True , blank=True)
    companyEmployeeCount = models.CharField(max_length=255, null=True , blank=True)
    companyType = models.CharField(max_length=255, null=True , blank=True)
    companyTicker = models.CharField(max_length=255, null=True , blank=True)
    companyRanking = models.CharField(max_length=255, null=True , blank=True)
    isDefunct = models.BooleanField(null=True , blank=True)
    companyPrimaryIndustry = models.CharField(max_length=255, null=True , blank=True)
    companyRevenueRange = models.CharField(max_length=255, null=True , blank=True)
    companyEmployeeRange = models.CharField(max_length=255, null=True , blank=True)
    locationCompanyId = models.CharField(max_length=255, null=True , blank=True)
    positionStartDate = models.CharField(max_length=255, null=True , blank=True)
    yearsOfExperience = models.IntegerField(null=True , blank=True)
    data_source = models.CharField(choices=(("linkedin_package","linkedin_package"),("linkedin_selenium","linkedin_selenium")),max_length=20)


class ContactHashedEmails(BaseModel):
    contactDetails = models.ForeignKey(ContactDetails, on_delete = models.PROTECT, related_name="contactHashedEmails")
    mail = models.EmailField()


class ContactExternalUrls(BaseModel):
    contactDetails = models.ForeignKey(ContactDetails, on_delete = models.PROTECT, related_name="contactExternalUrls")
    linkedIn = models.CharField(max_length=255, null=True , blank=True) #linkedin urls
    twitter = models.CharField(max_length=255, null=True , blank=True) #twitter urls


class ContactEmploymentHistory(BaseModel):
    contactDetails = models.ForeignKey(ContactDetails, on_delete = models.PROTECT, related_name="contactEmploymentHistory")
    companyName = models.CharField(max_length=255, null=True , blank=True) 
    jobTitle = models.CharField(max_length=255, null=True , blank=True) 
    startDate = models.CharField(max_length=255, null=True , blank=True) 
    endDate = models.CharField(max_length=255, null=True , blank=True)


class ContactCompanySocialMediaUrls(BaseModel):
    contactDetails = models.ForeignKey(ContactDetails, on_delete = models.PROTECT, related_name="contactCompanySocialMediaUrls")
    facebook = models.CharField(max_length=255, null=True , blank=True) #facebook urls of company
    linkedIn = models.CharField(max_length=255, null=True , blank=True) #linkedin urls of company


class ContactCompanyIndustries(BaseModel):
    contactDetails = models.ForeignKey(ContactDetails, on_delete = models.PROTECT, related_name="contactCompanyIndustries")
    name = models.CharField(max_length=255, null=True , blank=True) #industry name of company


class ContactTechSkills(BaseModel):
    contactDetails = models.ForeignKey(ContactDetails, on_delete = models.PROTECT, related_name="contactTechSkills")
    skill = models.CharField(max_length=255, null=True , blank=True)
   

class ContactSourceSystem(BaseModel):
    contactDetails = models.ForeignKey(ContactDetails, on_delete = models.PROTECT, related_name="contactSourceSystem")
    name = models.CharField(max_length=255, null=True , blank=True)
