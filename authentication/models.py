from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from mossala.utils import is_valid_phone_number

# Create your models here.
class UserStatus(models.Model):
    status = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='Status')

    def __str__(self):
        return self.status
    
    class Meta:
        verbose_name = 'Status'
        verbose_name_plural = 'Statuses'
        db_table = 'user_status'
        ordering = ['status']


class UserManager(BaseUserManager):
    def create_user(self, tel, password=None, **extra_fields):
        if not tel:
            raise ValueError('The Tel must be set')
        tel = is_valid_phone_number(tel)
        user = self.model(tel=tel, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='Nom d\'utilisateur')
    tel = models.CharField(max_length=15, unique=True, null=False, blank=False, verbose_name='Numéro de téléphone')
    email = models.EmailField(max_length=255, unique=True, null=False, blank=False, verbose_name='Email')
    email_verified = models.BooleanField(default=False, verbose_name='Email vérifié')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'inscription')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Dernière connexion')
    status = models.ManyToManyField(UserStatus, verbose_name='Status')
    is_staff = models.BooleanField(default=False, verbose_name='Staff')
    is_active = models.BooleanField(default=True, verbose_name='Actif')
    is_superuser = models.BooleanField(default=False, verbose_name='Superutilisateur')
    
    objects = UserManager()
    
    USERNAME_FIELD = 'tel'
    #REQUIRED_FIELDS = ['email']
    
    def __str__(self):
        return f"{self.username} - ({self.tel})"
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
        db_table = 'users'
        ordering = ['username', 'tel']
    
    def get_full_name(self):
        return self.username
    
    def get_short_name(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return self.is_superuser or super().has_perm(perm, obj)
    
    def has_module_perms(self, app_label):
        return self.is_superuser or super().has_module_perms(app_label)
    
    def has_role(self, status_name):
        """ Vérifie si l'utilisateur a un rôle spécifique """
        return self.status.filter(name=status_name).exists()
    
    def add_role(self, status_name):
        """ Ajoute un rôle à l'utilisateur """
        status = UserStatus.objects.get(name=status_name)
        self.status.add(status)
        self.save()
    
    def remove_role(self, status_name):
        """ Supprime un rôle à l'utilisateur """
        status = UserStatus.objects.get(name=status_name)
        self.status.remove(status)
        self.save()
    
    def get_roles(self):
        """ Récupère les rôles de l'utilisateur """
        return self.status.all()
    
    def update_roles(self, roles_names):
        """ Met à jour les rôles de l'utilisateur """
        roles = UserStatus.objects.filter(name__in=roles_names)
        self.status.set(roles)
        self.save()
    
    def reset_roles(self):
        """ Réinitialise les rôles de l'utilisateur """
        self.status.clear()
        self.save()
    
    def has_role(self, role_name):
        """ Vérifie si l'utilisateur a un rôle spécifique """
        return self.status.filter(name=role_name).exists()
    
    @property
    def is_authenticated(self):
        """ Vérifie si l'utilisateur est authentifié """
        return self.is_active
    
    def send_email_verification(self):
        """ Envoie un email de vérification pour l'utilisateur """
        # TODO: Implementer la fonctionnalité d'envoi d'email de vérification
        pass