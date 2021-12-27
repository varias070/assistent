from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', include('operator_ui.urls')),
    path('', admin.site.urls),
] + static(settings.STATIC_URL,)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
