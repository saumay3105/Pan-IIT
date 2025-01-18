from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/google/', views.GoogleSocialAuthView.as_view(), name='google_login'),
    re_path(r'^accounts/', include('allauth.urls'), name='socialaccount_signup'),
    # path("api/forgot-password", ForgotPasswordView.as_view(), name="forgotPassword"),
    # path("api/reset-password", ResetPasswordView.as_view(), name="resetPassword"),
]
