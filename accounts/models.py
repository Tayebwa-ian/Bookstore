from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser

# Accounts models are all created here

class CustomerUserManager(BaseUserManager):
	def create_user(self, email, password, **extra_fields):
		if not email:
			raise ValueError("The email must be set")

		email=self.normalize_email(email)
		user=self.model(email=email, **extra_fields)
		user.set_password(password)
		user.save()

		return user

	def create_superuser(self, email, password, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_active', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get("is_superuser")is not True:
			raise ValueError("is_superuser has to be set to True")
		if extra_fields.get("is_staff") is not True:
			raise ValueError("is_staff has to be set to True")
		if extra_fields.get("is_active") is not True:
			raise ValueError("is_active has to be set to True")

		return self.create_user(email, password, **extra_fields)

class User(AbstractUser):

	#creating new and extra user customised fields

	email=models.EmailField(unique=True, null=False, blank=False)
	username=models.CharField(max_length=50, null=True, blank=True)
	date_joined = models.DateField(auto_now_add=True)
	date_of_birth = models.DateField(null=True)
	is_customer=models.BooleanField(default=False)
	is_seller=models.BooleanField(default=False)
	telephone=models.IntegerField(null=True, blank=True)

	USERNAME_FIELD="email"
	REQUIRED_FIELDS=["username"]

	objects=CustomerUserManager()

	def __str__(self):
		return self.email