from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ProfileView, RegistrationView, activate, LoginView, LogoutView, EditProfileView, ChangePasswordView, ResetPasswordRequestView, ResetPasswordConfirmView, DeleteAccountView

router = DefaultRouter()
router.register('list', ProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('register/',RegistrationView.as_view(), name='register'),
    path('active/<uid64>/<token>/', activate, name = 'activate'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('edit/', EditProfileView.as_view(), name='edit'),
    path('change-password/', ChangePasswordView.as_view(), name='edit'),
    path('reset-password/', ResetPasswordRequestView.as_view(), name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('delete-account/', DeleteAccountView.as_view(), name='delete_account'),
]