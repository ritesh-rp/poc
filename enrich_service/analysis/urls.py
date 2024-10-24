from django.urls import path
from analysis.views import AnalysisBatch, ResultMapping ,ResultMappingBatch, ResultId



urlpatterns = [
    path("analysis/batch",AnalysisBatch.as_view(),name='analysisBatch'),
    path("result/mapping",ResultMapping.as_view(),name='resultMapping'),
    path("result/mapping/batch/",ResultMappingBatch.as_view(),name='resultMappingBatch'),
    path("result/id/",ResultId.as_view(),name='resultId'),
]