from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('', include('pages.urls')),
    path('hacker/', include('hacker.urls')),
    path('expert/', include('expert.urls')),
    path('company/', include('company.urls')),
    path('submission/', include('submission.urls'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
