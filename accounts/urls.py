from.import views
from django.urls import path

urlpatterns=[
 path("signup/", views.SignUpView.as_view(), name='signup'),
 path("login/", views.LoginView.as_view(), name='login'),
 path("logout/", views.signout, name='logout'),
 path("change-password/", views.ChangePasswordView.as_view(), name='change-password'),
 path("password-reset/<uidb64>/<token>/", views.PasswordTokenCheckView.as_view(), 
      name='password-reset-confirm'),
 path("request-password-reset/", views.RequestPasswordResetByEmail.as_view(), 
      name='request-password-reset'),
path("password-reset-complete/", views.SetNewPasswordAPIView.as_view(), 
      name='password-reset-complete'),
]