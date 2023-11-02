from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path("", views.api_root),
    path("credentials/", views.CredentialList.as_view(), name="credential_list"),
    path("credentials/<int:pk>/", views.CredentialDetail.as_view()),
    path("users/", views.UserList.as_view(), name="user_list"),
    path("users/profile/", views.UserDetail.as_view(), name="user_detail"),
    # path("users/pinAutentications",views.PinAuthenticationView.as_view(),name="user_pin_authentication"),
    path("login/",views.login_view,name="login_view"),
    path('randompass/',views.get_random_password,name="random_password"),
    path('mempass/',views.get_mem_password,name="mem_password"),
    path('passworddetail/',views.get_password_detail,name="password_pawn"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
