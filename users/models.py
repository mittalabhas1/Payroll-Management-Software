from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class CustomUserManager(BaseUserManager):
  def _create_user(self, username, email, password,
                     is_staff, is_superuser):
    """
    Creates and saves a User with the given email and password.
    """
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(username=username, email=email, is_staff=is_staff, is_active=True, is_superuser=is_superuser, last_login=now, date_joined=now)
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, username, email, password=None):
    return self._create_user(username, email, password, False, False)

  def create_superuser(self, username, email, password):
    return self._create_user(username, email, password, True, True)

class User(AbstractBaseUser, PermissionsMixin):
  """
  A fully featured User model with admin-compliant permissions that uses
  a full-length email field as the username.

  Email and password are required. Other fields are optional.
  """
  username = models.CharField(max_length=20, unique=True)
  email = models.EmailField(max_length=254)
  first_name = models.CharField(max_length=30, blank=True)
  last_name = models.CharField(max_length=30, blank=True)
  is_staff = models.BooleanField(default=False, help_text=('Designates whether the user can log into this admin site.'))
  is_active = models.BooleanField(default=True, help_text=('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
  date_joined = models.DateTimeField(default=timezone.now)

  objects = CustomUserManager()

  USERNAME_FIELD = 'username'
  REQUIRED_FIELDS = ['email']

  def get_full_name(self):
    """
    Returns the first_name plus the last_name, with a space in between.
    """
    full_name = '%s %s' % (self.first_name, self.last_name)
    return full_name.strip()

  def get_short_name(self):
    "Returns the short name for the user."
    return self.first_name
