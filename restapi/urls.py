from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from rest_framework import routers
from user.views import UserViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path(
        "google-oauth/", include(("google_auth.urls", "google-oauth"))
    ),
]
