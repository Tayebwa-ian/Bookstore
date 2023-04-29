from .models import User
from rest_framework import serializers
from rest_framework.validators import ValidationError
from rest_framework.authtoken.models import Token
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed

class SignUpSerializer(serializers.ModelSerializer):
	email=serializers.EmailField(required=True)
	username=serializers.CharField(max_length=40, min_length=3)
	password=serializers.CharField(min_length=8, write_only=True, style={'input_type':'password '})
	telephone= serializers.IntegerField()


	class Meta:
		model=User
		fields=['email', 'username', 'password', 'telephone']

	def validate(self, attrs):
		email_exists=User.objects.filter(email=attrs['email']).exists()
		if email_exists:
			raise ValidationError('The email used to SignUp already exists!')

		return super().validate(attrs)

	def create(self, validated_data):
		"""
		-This is to hash the password provided by the user
		-and create an authentication token for every user that is registered
		"""
		password=validated_data.pop('password')
		user=super().create(validated_data)
		user.set_password(password)
		user.save()
		Token.objects.create(user=user) #creating a unique token for the user

		return user

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True, 
                                         min_length=8, write_only=True, style={'input_type':'password '})
    new_password = serializers.CharField(required=True,
                                         min_length=8, write_only=True, style={'input_type':'password '})
    
class ResetPasswordByEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    class Meta:
        fields = ['email']
	
class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, write_only=True, 
                                     style={'input_type':'password '}, required=True)
    token = serializers.CharField(min_length=1, write_only=True, required=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True, required=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
			#decoding and making the result human readable
            id = force_str(urlsafe_base64_decode(uidb64))
            #get the owner the password to be changed
            user = User.objects.get(id=id)
            
            #check to see if token is valid
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)
			#set and save the new password
            user.set_password(password)
            user.save()

            return (user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)