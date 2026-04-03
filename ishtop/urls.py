from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from jobs.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),
    path('ishlar/', include('jobs.urls')),
    path('accounts/', include('accounts.urls')),
    path('chat/', include('chat.urls')),
    path('baholar/', include('ratings.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
