from django.db import models

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin

from mossala.utils import is_valid_phone_number


class District(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='Nom du district')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Arrondissement'
        verbose_name_plural = 'Arrondissements'
        db_table = 'arrondissement'
        ordering = ['name']

class Quater(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False, verbose_name='Nom du quartier')
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name='Arrondissement')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Quartier'
        verbose_name_plural = 'Quartiers'
        db_table = 'quartier'
        ordering = ['name']


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
        
        if not is_valid_phone_number(tel):
            raise ValueError('The Tel is not valid')
        user = self.model(tel=tel, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tel, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(tel, password, **extra_fields)



class UserProfile(models.Model):
    lastname = models.CharField(max_length=50, verbose_name="Nom", null=True, blank=True)
    firstname = models.CharField(max_length=50, verbose_name="Prénom", null=True, blank=True)
    nickname = models.CharField(max_length=50, verbose_name="Surnom", null=True, blank=True)
    gender = models.CharField(max_length=10,  verbose_name="Sexe", null=True, blank=True)
    nationality = models.CharField(max_length=50, verbose_name="Nationalité", null=True, blank=True)
    birthplace = models.CharField(max_length=100, verbose_name="Lieu de naissance", null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name="Adresse", null=True, blank=True)
    date_of_birth = models.DateField(verbose_name="Date de naissance", null=True, blank=True)
    photo = models.ImageField(upload_to='profiles/', verbose_name="Photo", null=True, blank=True)
    skype = models.CharField(max_length=50, verbose_name="Skype", null=True, blank=True)
    gmail = models.EmailField(verbose_name="Gmail", null=True, blank=True)
    discord = models.URLField(verbose_name="Discord", null=True, blank=True)
    whatsapp = models.CharField(max_length=20, verbose_name="WhatsApp", null=True, blank=True)
    facebook = models.URLField(verbose_name="Facebook", null=True, blank=True)
    twitter = models.URLField(verbose_name="Twitter", null=True, blank=True)
    instagram = models.URLField(verbose_name="Instagram", null=True, blank=True)
    linkedin = models.URLField(verbose_name="LinkedIn", null=True, blank=True)
    phone_work = models.CharField(max_length=20, verbose_name="Téléphone professionnel", null=True, blank=True)
    profession = models.CharField(max_length=50, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class User(AbstractBaseUser, PermissionsMixin, UserProfile):
    username = models.CharField(max_length=50, unique=True, null=True, blank=True, verbose_name='Nom d\'utilisateur')
    tel = models.CharField(max_length=15, unique=True, null=False, blank=False, verbose_name='Numéro de téléphone')
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True, verbose_name='Email')
    email_verified = models.BooleanField(default=False, verbose_name='Email vérifié')
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'inscription')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Dernière connexion')
    user_quater = models.ForeignKey(Quater, on_delete=models.SET_NULL, null=True, blank=True)
    last_ip = models.GenericIPAddressField(null=True, blank=True)
    last_location = models.CharField(max_length=255, null=True, blank=True)
    imei = models.CharField(max_length=50, null=True, blank=True)
    is_verified = models.BooleanField(default=False, verbose_name='Vérifié')
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