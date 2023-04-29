from django.contrib.auth import authenticate, logout
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.request import Request
from .serializers import *
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .util import EmailToSend
# Create your views here.
class SignUpView(generics.GenericAPIView):
	serializer_class= SignUpSerializer
	permission_classes=[]

	def post(self, request: Request):
		data=request.data
		serializer=self.serializer_class(data=data)
		if serializer.is_valid():
			serializer.save()
			response={
			"message": "Sign Up successful",
			"data": serializer.data
			}
			return Response(data=response, status=status.HTTP_201_CREATED)

		return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
	
	permission_classes=[]

	def post(self, request:Request):
		email=request.data.get('email')
		password=request.data.get('password')
		user=authenticate(email=email, password=password)

		if user is not None:
			response={
			'message': 'Successful Login',
			'token': user.auth_token.key,
			}

			return Response(data=response, status=status.HTTP_200_OK)
		else:
			return Response(data={'message':'Invalid Email or Password'})

	def get(self, request:Request):
		# just exploring the request content
		content={
		 "User": str(request.user),
		 "Token": str(request.auth),
		 }

		return Response(data=content, status=status.HTTP_200_OK)

@api_view(["GET"])	
@permission_classes([IsAuthenticated])
def signout(request:Request):
	if request.user:
		request.user.auth_token.delete()
		logout(request)
		return Response(data={"message": "Successfully signed out"})
	
class ChangePasswordView(generics.UpdateAPIView):
	"""
	-End point for user changing their password
	"""
	model=User
	serializer_class=ChangePasswordSerializer
	permission_classes=[IsAuthenticated]

	def get_object(self):
		obj=self.request.user
		return obj
	
	def update(self, request, *args, **kwargs):
		self.object= self.get_object()
		serialiazer=self.get_serializer(data=request.data)

		if serialiazer.is_valid():
			#check old password
			if self.object.check_password(serialiazer.data.get("old_password")) is False:
				return Response({"old password": ["wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
			#set and hash new password using set_password method
			self.object.set_password(serialiazer.data.get('new_password'))
			self.object.save()
			response={
				"message":"password changed successfully"
			}
			return Response(data=response, status=status.HTTP_200_OK)
		return Response(data=serialiazer.errors, status=status.HTTP_400_BAD_REQUEST)
	
class RequestPasswordResetByEmail(generics.GenericAPIView):
	serializer_class=ResetPasswordByEmailSerializer

	def post(self, request:Request):
		serializer=self.serializer_class(data=request.data)
		serializer.is_valid(raise_exception=True)

		email = request.data.get('email')
		if User.objects.filter(email=email).exists():
			user = User.objects.get(email=email)
			uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
			token = PasswordResetTokenGenerator().make_token(user)
			# damain name of the current site
			current_site = get_current_site(
                request=request).domain
			
			relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
			absurl = 'http://'+current_site + relativeLink
			email_body = 'Hello, \n Use link below to reset your password  \n' + absurl
			data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset your passsword'}
			EmailToSend.send_email(data)
			return Response({'success': 'We have sent you a link to reset your password'}, 
		   status=status.HTTP_200_OK)
		return Response({'failed': 'This email does not have and account with us, Kindly register'}, 
		   status=status.HTTP_404_NOT_FOUND)


class PasswordTokenCheckView(generics.GenericAPIView):
	"""
	Upon the user clicking on the link sent via email these checks are performed
		-if token was tempered with
		-if token is valid
		-if token was used before
	"""
	def get(self, request, uidb64, token):
		try:
			id=smart_str(urlsafe_base64_decode(uidb64))
			user=User.objects.get(id=id)

			if not PasswordResetTokenGenerator().check_token(user, token):
				return Response({"error":"Token is no valid please request a new one"})
			data={
				"token": token,
				"uidb64": uidb64,
				"message": "Valid Credentials"
			}
			return Response(data=data, status=status.HTTP_200_OK)
		except DjangoUnicodeDecodeError:
			return Response({"error":"Token is no valid please request a new one"}, 
		   status=status.HTTP_400_BAD_REQUEST)
		
class SetNewPasswordAPIView(generics.GenericAPIView):
    """
	This endpoint handles changing password to a new one
	"""
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Password reset successful'}, status=status.HTTP_200_OK)
		
