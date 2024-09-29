from django.urls import include, path

login_urlpatterns = [
    path(
        "sdk/",
        include(("google_auth.sdk.urls", "login")),
    ),
]

urlpatterns = [
    path("login/", include(login_urlpatterns)),
]
