from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create a custom user manager for the custom user
        """
        
        if not email:
            raise ValueError(_("An email is required."))
            
        user = self.model(
            email = self.normalize_email(email),
            **extra_fields,
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        """Create a super with the CustomUser model

        Args:
            email (string): A unique email for user identification
            password (string, optional): A password for the user account. Defaults to None.
        """
        
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        
        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))
        
        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name="email field", max_length=256, unique=True)
    is_active = models.BooleanField(
        _("active"), 
        default=True, 
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
            ),
        )
    is_staff = models.BooleanField(
        _("staff status"), 
        default=False, 
        help_text=_(
            "Designates whether the user can log into this admin site."
            ),
        )
    account_created = models.DateTimeField(_("date joined"), default=timezone.now)
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    display_name = models.CharField(_("display name"), max_length=150, blank=True)
    
    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()