import random, time

from linkedin_api import Linkedin
from decouple import config
from utilities.selenium_methods.get_url import get_urls_google_scraping
from utilities.selenium_methods.yahoo_finance import scrap_yahooFinance
from num2words import num2words

LinkedInCredentialsList = [{"LINKEDIN_EMAIL" :  "seanmendezdev@gmail.com"   ,  "LINKEDIN_PASSWORD": "ajaz78601"},
                            {"LINKEDIN_EMAIL":  "raptorx2024@gmail.com"   ,  "LINKEDIN_PASSWORD": "00998877@123 @@"},
                            {"LINKEDIN_EMAIL":  "dm759643@gmail.com"   ,  "LINKEDIN_PASSWORD": "mb7793907"},
                            ]
                            # {"LINKEDIN_EMAIL":  "jay920879@gmail.com"   ,  "LINKEDIN_PASSWORD": "rana2468"},


def get_contact_profile_details(username,companyName=""):
    try:
        # Add a random time delay between 2 to 8 minutes
        random_delay = random.randint(120, 500)  # Random time between 2 to 10 minutes (in seconds)
        time.sleep(random_delay)
        # Generate a random index to choose a random object from the list
        random_index = random.randint(0, len(LinkedInCredentialsList) - 1)
        linkedinClient = Linkedin(LinkedInCredentialsList[random_index]["LINKEDIN_EMAIL"],LinkedInCredentialsList[random_index]["LINKEDIN_PASSWORD"])

        print("username",username)
        # fetching profile data
        result = linkedinClient.get_profile(username)
        # fetching contact details i.e. phone and email
        contacts = linkedinClient.get_profile_contact_info(username)
        print("User contact details fetched ===================")
        # fetching contact skills
        skills = linkedinClient.get_profile_skills(username)
        print("User skills fetched ===================")

        all_contact_details = {}
        if not result :
            response = {"error":"enter valid username","username":username,"status":400}
            return response
        if not companyName:
            companyName = result.get("experience",[])[0].get("companyName","") if result.get("experience",[]) else ""
        # fetching company username by google scraping
        company_username = get_urls_google_scraping(companyName + "LinkedIn")        
        # fetching company details 
        company = linkedinClient.get_company(company_username)
        print("company details fetched ===================")
        # scraping yahoo finance to get details company's phone, revenue , ticker id, industries
        yahoo_finance = scrap_yahooFinance(companyName)
        print("yahoo_finance scraping done ===================")
        # organising the data in the specific format
        contact_details = {}
        contact_details["firstName"] = result.get("firstName","")
        contact_details["middleName"] = result.get("middleName","")
        contact_details["lastName"] = result.get("lastName","")
        contact_details["email"] = contacts.get("email_address","")
        contact_details["hasCanadianEmail"]   = False
        if contact_details["email"]:
            contact_details["hasCanadianEmail"] = True if contact_details["email"][-3:] == ".ca" else False
        contact_details["phone"] = contacts.get("phone_numbers", [])[0].get("number", "") if contacts.get("phone_numbers", []) else ""
        contact_details["directPhoneDoNotCall"] = ""
        contact_details["street"] = ""
        contact_details["city"] = ""
        contact_details["state"] = ""
        if result.get("geoLocationName"):
            contact_details["city"] = result.get("geoLocationName","").split(",")[0]
            contact_details["state"] = result.get("geoLocationName","").split(",")[1] if len(result.get("geoLocationName","").split(","))>1 else ""
        contact_details["region"] = ""
        contact_details["metroArea"] = ""
        contact_details["zipCode"] = ""
        contact_details["country"] = result.get("geoCountryName","")
        contact_details["continent"] = ""
        companyCity = result.get("experience",[])[0].get("companyName","") if result.get("experience",[]) else ""
        contact_details["personHasMoved"] = False if contact_details["city"] == companyCity else True
        contact_details["withinEu"] = ""
        contact_details["withinCalifornia"] = True if (contact_details["country"]).lower() == "california" else False
        contact_details["withinCanada"] = True if (contact_details["country"]).lower() == "canada" else False
        # contact_details["validDate"] = ""
        # contact_details["lastUpdatedDate"] = ""
        # contact_details["noticeProvidedDate"] = ""
        contact_details["salutation"] =  ""
        contact_details["suffix"] = ""
        contact_details["jobTitle"] = result.get("experience",[])[0].get("title","") if result.get("experience",[]) else ""
        contact_details["jobFunction"] = ""
        contact_details["education"] =  result.get("education",[])[0].get("degreeName","") if result.get("education",[]) else ""
        contact_details["picture"] = result.get("displayPictureUrl","")+result.get("img_400_400","")
        contact_details["mobilePhoneDoNotCall"] = ""
        contact_details["managementLevel"] = ""
        # contact_details["contactAccuracyScore"] = None
        contact_details["companyId"] = ""
        contact_details["companyName"] = result.get("experience",[])[0].get("companyName","") if result.get("experience",[]) else ""
        contact_details["companyDescriptionList"] = company["description"]
        contact_details["companyPhone"] = yahoo_finance.get("company_phone","")
        contact_details["companyFax"] = ""
        contact_details["companyStreet"] = ""

        try:
            contact_details["companyCity"] = result.get("experience",[])[0].get("geoLocationName","").split(",")[0] if result.get("experience",[]) else ""
        except:
            contact_details["companyCity"] = ""
        try:
            contact_details["companyState"] = result.get("experience",[])[0].get("geoLocationName","").split(",")[1] if result.get("experience",[]) else ""
        except:
            contact_details["companyState"] = contact_details["companyCity"]


        contact_details["companyZipCode"] = ""
        contact_details["companyCountry"] = ""
        for i in company.get("confirmedLocations",[]):
            if i.get("geographicArea","").lower() == contact_details["companyState"].lower():
                contact_details["companyZipCode"] = i.get("postalCode","")
                contact_details["companyCountry"] = i.get("country","")
        contact_details["companyContinent"] = ""
        contact_details["companyLogo"] = company.get("logo",{}).get("image",{}).get("com.linkedin.common.VectorImage",{}).get("rootUrl","")+company.get("logo",{}).get("image",{}).get("com.linkedin.common.VectorImage",{}).get("artifacts",[])[0].get("fileIdentifyingUrlPathSegment","")
        contact_details["companyDivision"] = ""
        contact_details["companySicCodes"] = ""
        contact_details["companyNaicsCodes"] = ""
        contact_details["companyWebsite"] = company.get("callToAction",{}).get("url","")
        contact_details["companyRevenue"] = ""
        contact_details["companyRevenueNumeric"] = int(yahoo_finance.get("revenue")) if yahoo_finance.get("revenue") else None
        if contact_details["companyRevenueNumeric"]:
            contact_details["companyRevenue"] = num2words(contact_details["companyRevenueNumeric"])
        contact_details["companyEmployeeCount"] = str(company.get("staffCountRange",{}).get("start","")) + "-" + str(company.get("staffCountRange",{}).get("end",""))
        contact_details["companyType"] = company.get("companyType",{}).get("localizedName","")
        contact_details["companyTicker"] = yahoo_finance.get("ticker","")
        contact_details["companyRanking"] = ""
        contact_details["isDefunct"] = ""
        contact_details["companyPrimaryIndustry"] = company.get("companyIndustries",[])[0].get("localizedName","") if company.get("companyIndustries",[]) else ""
        contact_details["companyRevenueRange"] = yahoo_finance.get("revenue_range","")
        contact_details["companyEmployeeRange"] = str(company.get("staffCountRange",{}).get("start","")) + "-" + str(company.get("staffCountRange",{}).get("end",""))
        contact_details["locationCompanyId"] = ""
        contact_details["positionStartDate"] = ""
        # contact_details["yearsOfExperience"] = 
        ContactEmploymentHistory = []
        if result["experience"]:
            first_item = result["experience"][0]
            contact_details["positionStartDate"] = str(first_item.get("timePeriod",{}).get("startDate",{}).get("year","")) + "-" + str(first_item.get("timePeriod",{}).get("startDate",{}).get("month",""))+"-01" if result["experience"] else None

            for item in result["experience"]:
                EmploymentHistory = {}
                EmploymentHistory["companyName"] = item["companyName"]
                EmploymentHistory["jobTitle"] = item["title"]
                EmploymentHistory["startDate"] = str(item.get("timePeriod",{}).get("startDate",{}).get("month","")) + "/" + str(item.get("timePeriod",{}).get("startDate",{}).get("year","")) 
                if item.get("timePeriod",{}).get("endDate",{}):
                    EmploymentHistory["endDate"] = str(item.get("timePeriod",{}).get("endDate",{}).get("month","")) + "/" + str(item.get("timePeriod",{}).get("endDate",{}).get("year","")) 
                else:
                    EmploymentHistory["endDate"] = "Present"
                ContactEmploymentHistory.append(EmploymentHistory)
        # combining the details together to return
        all_contact_details["contact_details"]=contact_details
        all_contact_details["ContactEmploymentHistory"]= ContactEmploymentHistory
        all_contact_details["skills"] = skills
        all_contact_details["industries"] = yahoo_finance["industry"]

        return all_contact_details
    except Exception as E:
        print("Function error===============================> {} {} {}".format(E,LinkedInCredentialsList[random_index]["LINKEDIN_EMAIL"],LinkedInCredentialsList[random_index]["LINKEDIN_PASSWORD"]))
        return {"username":username,"error":str(E),"status":500}