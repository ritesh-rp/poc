from django.contrib import admin
from django.urls import path, include
from enrich_service.views import Homepage, Profiles, ScrapedData
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="Enrich Data API's",
        default_version='v1',
        description="API's for getting user and company's data",
        terms_of_service="https://www.example.com/policies/terms/",
        contact=openapi.Contact(email="contact@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    patterns=[
        path('api/', include('analysis.urls')),
    ]
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/",include("analysis.urls")),
    path("", Homepage.as_view()),
    path("batches/", Homepage.as_view()),
    path("batch_profiles/<int:batch_id>", Profiles.as_view()),
    path("data/<str:batch_id>/<str:uuid>", ScrapedData.as_view()),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),


]

