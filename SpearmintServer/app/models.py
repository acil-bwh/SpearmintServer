from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)

# decorator to make app models hidden (i.e. not shown to normal users)
def hidden(app_model_class):
    @classmethod
    def hidden(cls, user):
        return not user.is_admin
    setattr(app_model_class, 'hidden', hidden)
    return app_model_class

# -----------------------------------------------------------------------------
#
# Custom User Manager (django admin compliant)
#
# see https://docs.djangoproject.com/en/1.6/topics/auth/customizing/
#
# -----------------------------------------------------------------------------

class UserManager(BaseUserManager):
    def create_user(self, username, email, institution, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not username:
            raise ValueError('Users must have a username')

        if not email:
            raise ValueError('Users must have an email address')

        if not institution:
            raise ValueError('Users must have an institution name')

        user = self.model(
            username = username,
            email = self.normalize_email(email),
            institution = institution,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, institution, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(username, email,
            password=password,
            institution=institution
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

# -----------------------------------------------------------------------------
#
# Custom User Model (django admin compliant)
#
# see https://docs.djangoproject.com/en/1.6/topics/auth/customizing/
#
# -----------------------------------------------------------------------------

@hidden
class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    creation_date = models.DateTimeField(auto_now=True)
    institution = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'institution']

    def get_full_name(self):
        # The user is identified by their username
        return self.username

    def get_short_name(self):
        # The user is identified by their username
        return self.username

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @staticmethod
    def display_order():
        return 'username'

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

class MongoDB(models.Model):
    db_address = models.CharField(max_length=50, default='spmint.chestimagingplatform.org')
    username = models.CharField(max_length=20,default='')
    password = models.CharField(max_length=20, default='')

