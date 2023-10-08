from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # path("credentials/", views.CredentialList.as_view()),
    path("credentials/<int:pk>/", views.CredentialDetail.as_view()),
    path("users/<int:pk>/", views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
