from celery import shared_task
from utilities.selenium_methods.get_url import get_urls_google_scraping
from analysis.models import BatchProfilePayload ,ContactDetails ,ContactEmploymentHistory,ContactTechSkills,ContactCompanyIndustries
from utilities.linkedinPackage.get_contact_details import get_contact_profile_details


@shared_task
def profileEnrich(uuid_list):
    try:
        pending_Batches = BatchProfilePayload.objects.filter(batchProfile__profile__uuid__in = uuid_list,status = "Pending").values("id","batchProfile__profile__uuid")
        # filtering the latest uuid from pending_Batches objects
        dict_obj = {}
        for obj in pending_Batches:
            if obj["batchProfile__profile__uuid"] in dict_obj and obj["id"] < dict_obj[obj["batchProfile__profile__uuid"]]:
                pass
            else:
                dict_obj[obj["batchProfile__profile__uuid"]] = obj["id"]

        required_uuid = []
        for key,value in dict_obj.items():
            required_uuid.append(value)
        
        pending_contact_batches = BatchProfilePayload.objects.filter(id__in = required_uuid)

        for pending_contact_batch in pending_contact_batches:
            try:
                # get username of profile by google selenium
                contact_username = get_urls_google_scraping("'"+pending_contact_batch.fullName+"'"+' LinkedIn ' + pending_contact_batch.companyName)  
                contact_data = get_contact_profile_details(contact_username[0],pending_contact_batch.companyName)
                contact_obj = ContactDetails.objects.create(**contact_data["contact_details"],batchProfilePayload = pending_contact_batch,data_source ="linkedin_package" )
                contact_obj.save()
                for item in contact_data["ContactEmploymentHistory"]:
                    ContactEmploymentHistory_obj = ContactEmploymentHistory.objects.create(**item,contactDetails = contact_obj)
                    ContactEmploymentHistory_obj.save()
                for skill in contact_data["skills"]:
                    contactTechSkills_obj = ContactTechSkills.objects.create(skill = skill["name"],contactDetails = contact_obj)
                    contactTechSkills_obj.save()
                for industry in contact_data["industries"]:
                    contactCompanyIndustries_obj = ContactCompanyIndustries.objects.create(name = industry,contactDetails = contact_obj)
                    contactCompanyIndustries_obj.save()
                pending_contact_batch.status = "completed"
                pending_contact_batch.save()
            except Exception as E:
                pending_contact_batch.status = "Failed"
                pending_contact_batch.save()
                print("Unable to process profile {}".format(E))
        return "Data saved to db"
    except Exception as e:
        print("error==========================>",e)
        return str(e)
    