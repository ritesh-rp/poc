from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.authentication import authenticate ,SessionAuthentication
from rest_framework.permissions import IsAdminUser ,IsAuthenticated, AllowAny
from django.contrib.auth.mixins import LoginRequiredMixin 
from analysis.models import *
from django.db.models import F,Q
from django.core.paginator import Paginator



class Homepage(APIView):
    # login_url="/login"
    # authentication_classes=[SessionAuthentication]
    # permission_classes=[IsAuthenticated]
    def get(self, request):
        try:
            # Show the list of batches
            batches_objects = Batch.objects.filter().values("id","created_on").order_by("-id")
            # pagination
            page = request.GET.get("page","1")
            paginator = Paginator(batches_objects, 10)
            batches = paginator.page(page)

            return render(request, "batchlists.html",{"batch_data":batches})
        except Exception as e:
            print(str(e))
            return render(request, "batchlists.html", {"errors": str(e)})

    def post(self, request):
        try:
            batch_id = request.POST.get("batch_id","")
            batches_obj = Batch.objects.filter(id = batch_id).values("id","created_on").order_by("-id")
            # pagination
            page = request.GET.get("page","1")
            paginator = Paginator(batches_obj, 10)
            batches = paginator.page(page)
            #modification of date format 
            for batch in batches:
                batch["created_on"] = batch["created_on"].strftime("%Y-%m-%d  %H:%M:%S")
            return render(request, "batchlists.html",{"batch_data":batches,"batch_id":batch_id})
        except Exception as e:
            print(str(e))
            return render(request, "batchlists.html", {"errors": str(e)})    

class Profiles(APIView):
    # login_url="/login"
    # authentication_classes=[SessionAuthentication]
    # permission_classes=[IsAuthenticated]
    def get(self, request,batch_id):
        try:
            # Show the profile data from batch id
            profiles_objects = Profile.objects.filter(batchProfile__batch__id=batch_id).values("uuid","batchProfile__batchprofilepayload__fullName","migrationId","tableName","recordId").annotate(status = F("batchProfile__batchprofilepayload__status")).order_by("-uuid")
            # pagination
            status = request.GET.get('status',"")
            page = request.GET.get("page","1")
            paginator = Paginator(profiles_objects, 10)
            profiles = paginator.page(page)
            return render(request, "profile.html",{"profiles":profiles,"batch_id":batch_id, "status":status})
        except Exception as e:
            print(str(e))
            return render(request, "profile.html", {"errors": str(e)})
    
    def post(self, request,batch_id):
        try:
            # searching profile by uuid and full-name 
            search_item = request.POST.get("search_item","")
            profiles_objects = Profile.objects.filter(batchProfile__batch__id=batch_id,batchProfile__batchprofilepayload__fullName__icontains = search_item).values("uuid","batchProfile__batchprofilepayload__fullName","migrationId","tableName","recordId").annotate(status = F("batchProfile__batchprofilepayload__status")).order_by("-uuid")
            try:
                profiles_objects = Profile.objects.filter(batchProfile__batch__id=batch_id,uuid = search_item).values("uuid","batchProfile__batchprofilepayload__fullName","migrationId","tableName","recordId").annotate(status = F("batchProfile__batchprofilepayload__status")).order_by("-uuid")
            except:
                pass
            # pagination
            page = request.GET.get("page","1")
            paginator = Paginator(profiles_objects, 10)
            profiles = paginator.page(page)
            return render(request, "profile.html",{"profiles":profiles,"search_item":search_item,"batch_id":batch_id})
        except Exception as e:
            print("error is=====================>",str(e))
            return render(request, "profile.html", {"errors": str(e),"search_item":search_item,"batch_id":batch_id})
        


class ScrapedData(APIView):
    # login_url="/login"
    # authentication_classes=[SessionAuthentication]
    # permission_classes=[IsAuthenticated]
    def get(self, request, batch_id, uuid):
        try:
            # records fetching related to profile
            contactDetails_latest = ContactDetails.objects.filter(batchProfilePayload__batchProfile__profile__uuid = uuid).values().last()
            contactExternalUrls = ContactExternalUrls.objects.filter(contactDetails = contactDetails_latest["id"]).values("linkedIn","twitter")
            contactHashedEmails = ContactHashedEmails.objects.filter(contactDetails = contactDetails_latest["id"]).values("mail")
            contactEmploymentHistory = ContactEmploymentHistory.objects.filter(contactDetails = contactDetails_latest["id"]).values("companyName","jobTitle","startDate","endDate")
            contactCompanySocialMediaUrls = ContactCompanySocialMediaUrls.objects.filter(contactDetails = contactDetails_latest["id"]).values("facebook","linkedIn")
            contactCompanyIndustries = ContactCompanyIndustries.objects.filter(contactDetails = contactDetails_latest["id"]).values("name")
            contactTechSkills = ContactTechSkills.objects.filter(contactDetails = contactDetails_latest["id"]).values("skill")
            contactSourceSystem = ContactSourceSystem.objects.filter(contactDetails = contactDetails_latest["id"]).values("name")
            
            # organising data of profile
            data = contactDetails_latest
            data["contactExternalUrls"] = contactExternalUrls
            data["contactHashedEmails"] = contactHashedEmails
            data["contactEmploymentHistory"] = contactEmploymentHistory
            data["contactCompanySocialMediaUrls"] = contactCompanySocialMediaUrls
            data["contactCompanyIndustries"] = contactCompanyIndustries
            data["contactTechSkills"] = contactTechSkills
            data["contactSourceSystem"] = contactSourceSystem
            return render(request, "scraped_data.html",{"scraped_data":data,"uuid":uuid,"batch_id":batch_id})
            
        except Exception as e:
            print(str(e))
            return render(request, "scraped_data.html", {"scraped_data":{},"uuid":uuid,"batch_id":batch_id,"errors": str(e)})