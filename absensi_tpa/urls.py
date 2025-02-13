from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('auth/', include('logreg.urls')),
    path('siswa/', include('siswa.urls')),
    path('admintpa/', include('admintpa.urls')),
    path('guru/', include('guru.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)