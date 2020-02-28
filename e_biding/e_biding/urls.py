from django.conf.urls.static import static
from django.urls import path, include
from admin import urls
from e_biding import settings

urlpatterns = [
    path('', include(urls)),
    path('', include('user.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
