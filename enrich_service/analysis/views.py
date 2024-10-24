from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from analysis.serializers import ContactBatchSerializer
from analysis.models import *
from django.db.models import Q
from utilities.tools import is_valid_email
from analysis.tasks import profileEnrich
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi



def get_results(profile):
    try:
        # records fetching related to profile
        contactDetails_latest = ContactDetails.objects.filter(batchProfilePayload__batchProfile__profile__uuid = profile.uuid).values().last()
        contactExternalUrls = ContactExternalUrls.objects.filter(contactDetails = contactDetails_latest["id"]).values("linkedIn","twitter")
        contactHashedEmails = ContactHashedEmails.objects.filter(contactDetails = contactDetails_latest["id"]).values("mail")
        contactEmploymentHistory = ContactEmploymentHistory.objects.filter(contactDetails = contactDetails_latest["id"]).values("companyName","jobTitle","startDate","endDate")
        contactCompanySocialMediaUrls = ContactCompanySocialMediaUrls.objects.filter(contactDetails = contactDetails_latest["id"]).values("facebook","linkedIn")
        contactCompanyIndustries = ContactCompanyIndustries.objects.filter(contactDetails = contactDetails_latest["id"]).values("name")
        contactTechSkills = ContactTechSkills.objects.filter(contactDetails = contactDetails_latest["id"]).values("skill")
        contactSourceSystem = ContactSourceSystem.objects.filter(contactDetails = contactDetails_latest["id"]).values("name")        # organising profile data
        
        contactTechSkills_lst = []

        if contactTechSkills:
            for items in contactTechSkills:
                for key,value in items.items():
                    contactTechSkills_lst.append(value)

        result_data = {}
        result_data["profileDetails"] = contactDetails_latest
        result_data["contactExternalUrls"] = contactExternalUrls
        result_data["contactHashedEmails"] = contactHashedEmails
        result_data["contactEmploymentHistory"] = contactEmploymentHistory
        result_data["contactCompanySocialMediaUrls"] = contactCompanySocialMediaUrls
        result_data["contactCompanyIndustries"] = contactCompanyIndustries
        result_data["contactTechSkills"] = contactTechSkills_lst
        result_data["contactSourceSystem"] = contactSourceSystem
        return result_data
    except:
        return {}


class AnalysisBatch(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: 'Success'},
        operation_id='My API View'
    )
    def post(self,request):
        try:
            payload = request.data.get("request","")
            if not payload:
                res = {"message":"Please enter a valid payload","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            response_data = {"successful":[],"unsuccessful":[]}

            contact_payloads = []
            company_payloads = []
            uuid_list = []

            # verifying email from payload
            valid_email_response = is_valid_email(payload)
            if valid_email_response["unsuccessful"]:
                res = {"message":"Something went wrong","success":"False","data":valid_email_response}
                return Response(res,status= status.HTTP_400_BAD_REQUEST)
            
            batch_obj = Batch.objects.create(data = payload)
            batch_obj.save()
            #filtering the data on the bases of contact and company
            for item in payload:
                if item["mapping"]["tableName"] == "Profile":
                    contact_payloads.append(item)
                elif item["mapping"]["tableName"] == "Account":
                    company_payloads.append(item)
            query = Q()
            for contact_payload in contact_payloads:
                for key, value in contact_payload["mapping"].items():
                    query |= Q(**{key: value})


            existing_profiles = Profile.objects.filter(query).values("migrationId","tableName","recordId")

            uuid_list = []
            for contact_payload in contact_payloads:
                # creating objects to store data
                try:
                    if contact_payload["mapping"] in existing_profiles:
                        print("profile_obj existing")
                        profile_obj = Profile.objects.filter(**contact_payload["mapping"]).first()
                        uuid_list.append(profile_obj.uuid)
                    else:
                        print("profile_obj doesnt exist")
                        profile_obj = Profile.objects.create(**contact_payload["mapping"])
                        profile_obj.save()
                        uuid_list.append(profile_obj.uuid)
                    batch_profile_obj = BatchProfile.objects.create(batch = batch_obj , profile = profile_obj)
                    batch_profile_obj.save()
                    BatchProfilePayload_obj = BatchProfilePayload.objects.create(**contact_payload["query"]["context"] , batchProfile = batch_profile_obj)
                    BatchProfilePayload_obj.save()
                    response_data["successful"].append({"migrationId":profile_obj.migrationId,"tableName":profile_obj.tableName,"recordId":profile_obj.recordId,"uuid":profile_obj.uuid})

                except Exception as e:
                    response_data["unsuccessful"].append({"migrationId":profile_obj.migrationId,"tableName":profile_obj.tableName,"recordId":profile_obj.recordId,"error":str(e)})

            # calling celery task
            profileEnrich.delay(uuid_list)
            res = {"message":"Batch Analysis registered successfully","success":"True","data":response_data}
            return Response(res,status=status.HTTP_200_OK)
        
        except Exception as e:
            print("error============================>",str(e))
            res = {"message":str(e),"success":"False","data":{}}
            return Response(res,status= status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResultMapping(APIView):
    def get(self,request):
        try:
            # collecting request data
            migrationId = request.GET.get("migrationId","")
            tableName = request.GET.get("tableName","")
            recordId = request.GET.get("recordId","")
            if not migrationId or not tableName or not recordId:
                res = {"message":"Please enter all details i.e migrationId,tableName,recordId","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            profile = Profile.objects.filter(migrationId = migrationId, tableName = tableName, recordId = recordId).last()
            # get details of profile by function
            if profile:
                result_data = get_results(profile)
                batchProfilePayload = BatchProfilePayload.objects.filter(batchProfile__profile__uuid = profile.uuid).last()
                mapping = {"migrationId":profile.migrationId, "tableName":profile.migrationId, "recordId" : profile.recordId,"uuid":profile.recordId}
                res = {"message":"Result ready","success":"true","data":{"status":batchProfilePayload.status,"mapping":mapping,"result":result_data}}
                return Response(res,status=status.HTTP_200_OK)
            else:
                res = {"message":"No records found","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error============================>",str(e))
            res = {"message":str(e),"success":"False","data":{}}
            return Response(res,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ResultMapping(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('migrationId', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Enter the migration ID'),
            openapi.Parameter('tableName', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Enter the table name'),
            openapi.Parameter('recordId', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Enter the record ID'),
        ],
        responses={200: 'Success'},
        operation_id='My API View'
    )
    def get(self,request):
        try:
            migrationId = request.GET.get("migrationId","")
            tableName = request.GET.get("tableName","")
            recordId = request.GET.get("recordId","")
            if not migrationId or not tableName or not recordId:
                res = {"message":"Please enter all details i.e migrationId,tableName,recordId","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            
            profile = Profile.objects.filter(migrationId = migrationId, tableName = tableName, recordId = recordId).last()
            # getting details from profile
            result_data = get_results(profile)
            if profile:
                batchProfilePayload = BatchProfilePayload.objects.filter(batchProfile__profile__uuid = profile.uuid).last()
                mapping = {"migrationId":profile.migrationId, "tableName":profile.tableName, "recordId" : profile.recordId,"uuid":profile.uuid}
                res = {"message":"Result ready","success":"true","data":{"status":batchProfilePayload.status,"mapping":mapping,"result":result_data}}
                return Response(res,status=status.HTTP_200_OK)
            else:
                res = {"message":"No records found","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error============================>",str(e))
            res = {"message":str(e),"success":"False","data":{}}
            return Response(res,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResultId(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('uuid', openapi.IN_QUERY, type=openapi.TYPE_STRING, description='Enter the uuid'),
        ],
        responses={200: 'Success'},
        operation_id='My API View'
    )
    def get(self,request):
        try:
            uuid = request.GET.get("uuid","")
            if not uuid:
                res = {"message":"Please enter UUID","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            profile = Profile.objects.filter(uuid = uuid).last()

            # getting details from profile
            result_data = get_results(profile)
            if profile:
                batchProfilePayload = BatchProfilePayload.objects.filter(batchProfile__profile__uuid = profile.uuid).last()
                mapping = {"migrationId":profile.migrationId, "tableName":profile.tableName, "recordId" : profile.recordId,"uuid":profile.uuid}
                res = {"message":"Result ready","success":"true","data":{"status":batchProfilePayload.status,"mapping":mapping,"result":result_data}}
                return Response(res,status=status.HTTP_200_OK)
            else:
                res = {"message":"No records found","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("error============================>",str(e))
            res = {"message":str(e),"success":"False","data":{}}
            return Response(res,status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResultMappingBatch(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER)
            }
        ),
        responses={200: 'Success'},
        operation_id='My API View'
    )
    def post(self,request):
        try:
            data = request.data.get("request")

            if not data:
                res = {"message":"Please give details","success":"False","data":{}}
                return Response(res,status=status.HTTP_400_BAD_REQUEST)
            final_res = {"message": "Result ready","success": "true","data": {"result":[]}}

            for item in data:
                profile = Profile.objects.filter(migrationId = item["migrationId"], tableName = item["tableName"], recordId = item["recordId"]).last()
                
                # getting details from profile
                result_data = get_results(profile)

                if profile:
                    batchProfilePayload = BatchProfilePayload.objects.filter(batchProfile__profile__uuid = profile.uuid).last()
                    mapping = {"migrationId":profile.migrationId, "tableName":profile.tableName, "recordId" : profile.recordId,"uuid":profile.uuid}
                    res = {"status":batchProfilePayload.status,"mapping":mapping,"result":result_data}
                    final_res["data"]["result"].append(res)
                else:
                    mapping = {"migrationId":item["migrationId"], "tableName":item["tableName"], "recordId" : item["recordId"]}
                    res = {"status":"not-found" ,"mapping":mapping,"result":{}}
                    final_res["data"]["result"].append(res)
            return Response(final_res,status=status.HTTP_200_OK)
            
        except Exception as e:
            print("error============================>",str(e))
            final_res = {"message": str(e),"success": "False","data": {"result":[]}}
            return Response(final_res,status=status.HTTP_500_INTERNAL_SERVER_ERROR)
