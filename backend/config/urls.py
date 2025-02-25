from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Create schema for Swagger/ReDoc API documentation
schema_view = get_schema_view(
    openapi.Info(
        title="Sports Event Management API",
        default_version='v1',
        description="API for the sports event management system",
        contact=openapi.Contact(email="contact@sportseventmanagement.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # Django admin
    path("admin/", admin.site.urls),
   
    # API Documentation
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
   
    # API authentication
    path('api/auth/', include('rest_framework.urls')),
   
    # JWT tokens
    path('api/token/', include('users.auth_urls')),
   
    # API apps
    path('api/users/', include('users.urls')),
    path('api/events/', include('events.urls')),
    path('api/teams/', include('teams.urls')),
    path('api/games/', include('games.urls')),
    path('api/scores/', include('scores.urls')),
    path('api/leaderboards/', include('leaderboards.urls')),
]

# Debug settings for development
if settings.DEBUG:
    # Add Debug Toolbar
    import debug_toolbar
    urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    
    # Serve static and media files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)