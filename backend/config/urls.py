from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

urlpatterns = [
     # Root URL for the welcome page
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # Django admin
    path("admin/", admin.site.urls),
   
    # API Documentation with drf-spectacular
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Backward compatibility for old URLs
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui-old'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc-old'),
   
    # API authentication
    path('api/auth/', include('rest_framework.urls')),
   
    path('accounts/', include('django.contrib.auth.urls')),
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