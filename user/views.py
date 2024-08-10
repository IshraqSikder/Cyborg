from rest_framework import viewsets, filters, generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Profile
from .serializers import ProfileSerializer, RegistrationSerializer, LoginSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.password_validation import validate_password
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMultiAlternatives, send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Create your views here.
BASE_URL_FRONT = "https://ishraqsikder.github.io/Cyborg-Client"
BASE_URL_BACKEND = "https://cyborg-gamezone.onrender.com"

class SearchByUserId(filters.BaseFilterBackend):
    def filter_queryset(self, request, query_set, view):
        # user_id = request.query_params.get("user_id")
        # if user_id:
        #     return query_set.filter(user = user_id)
        # return query_set
        user_id = request.query_params.get('user_id')
        if user_id:
            return query_set.filter(userName__id = user_id)
        return query_set
      
class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [SearchByUserId]
    
    # It is an another method to filter User using DjangoFilterBackend
    
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['userName']

class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    # permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"{BASE_URL_BACKEND}/clients/active/{uid}/{token}"
            # reset_link = request.build_absolute_uri(f'/clients/active/{uid}/{token}/')
            # reset_link = request.build_absolute_uri(reverse('activate', kwargs={'uidb64': uid, 'token': token}))
            email_subject = "Confirm Your Email"
            email_body = render_to_string('confirm_email.html', {'confirm_link' : confirm_link})
            email = EmailMultiAlternatives(email_subject , '', to=[user.email])
            email.attach_alternative(email_body, "text/html")
            email.send()
            return Response("Check your email for confirmation")
        return Response(serializer.errors)

def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user = None 
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been activated. You can now Sign In")
        return redirect(f'{BASE_URL_FRONT}/login.html')
    else:
        messages.error(request, "Invalid activation link")
        return redirect(f'{BASE_URL_FRONT}/register.html')
    
class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = self.request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)     
            if user:
                token, _ = Token.objects.get_or_create(user=user)
                login(request, user)
                return Response({'token' : token.key, 'user_id' : user.id, "detail": "Successfully logged in."})
            else:
                return Response({'error' : "Invalid Credential"})
        return Response(serializer.errors)

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            request.user.auth_token.delete()
            logout(request)
            return Response({'detail': 'Successfully logged out.'})
        except AttributeError:
            return Response({'error': 'The user is not logged in.'}, status=400)
    
class EditProfileView(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return Profile.objects.get(userName=self.request.user)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    
class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get('oldPassword')
        new_password = request.data.get('newPassword')
        confirm_password = request.data.get('confirmPassword')

        if not user.check_password(old_password):
            return Response({"errPassword": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"errPassword": "New passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(new_password, user)
        except Exception as e:
            return Response({"errPassword": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"detail": "Password changed successfully"}, status=status.HTTP_200_OK)
  
class ResetPasswordRequestView(APIView):
    def post(self, request):
        reset_email = request.data.get('reset_email')
        if not reset_email:
            return Response({'Email field is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=reset_email)
        except User.DoesNotExist:
            return Response({'No user is associated with this email address'}, status=status.HTTP_400_BAD_REQUEST)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        reset_link = f'{BASE_URL_FRONT}/reset_password_confirm.html?uidb64={uid}&token={token}'
        email_subject = 'Password Reset Requested'
        email_message = render_to_string('reset_password_email.html', {
            'user': user,
            'reset_link': reset_link,
        })
        send_mail(email_subject, email_message, settings.EMAIL_HOST_USER, [user.email])
        return Response('Password reset link has been sent to your email address', status=status.HTTP_200_OK)

class ResetPasswordConfirmView(APIView):
    def post(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            return Response({"Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({"Invalid reset token"}, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')

        if not new_password or not confirm_password:
            return Response({"Password fields cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)

        if new_password != confirm_password:
            return Response({"Passwords do not match"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"Password has been reset successfully"}, status=status.HTTP_200_OK)
    
class DeleteAccountView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        password = request.data.get('password')
        
        if not user.check_password(password):
            return Response({"Password does not match"}, status=status.HTTP_400_BAD_REQUEST)
        
        user.delete()
        return Response({"Account successfully deleted"}, status=status.HTTP_200_OK)