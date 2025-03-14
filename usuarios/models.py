from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from adscripcion.models import AreaAdscripcion

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, role='user', **extra_fields):
        """Crea un usuario normal con su respectivo rol."""
        if not username:
            raise ValueError("El usuario debe tener un nombre de usuario")
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        """Crea un superusuario con permisos de staff y superuser."""
        extra_fields.setdefault('role', 'superuser')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('estado', 'activo')

        return self.create_user(username, password, **extra_fields)
    
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Administrador'),
        ('user', 'Docente'),
        ('superuser', 'Super Usuario'),
)

    TIPO_DOCENTE_CHOICES = (
        ('basificado', 'Basificado'),
        ('asignatura', 'basificado'),
    )

    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tipo_docente = models.CharField(max_length=20, choices=TIPO_DOCENTE_CHOICES, null=True, blank=True)
    area_adscripcion = models.ForeignKey(
        AreaAdscripcion, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='usuarios_custom'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="usuarios_groups"
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="usuarios_permissions"
    )
    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """Otorga privilegios de staff a los superusuarios automáticamente"""
        if self.role == 'superuser': 
            self.is_staff = True
            self.is_superuser = True
        elif self.role == 'admin':
            self.is_staff = True
            self.is_superuser = False
        else:
            self.is_staff = False
            self.is_superuser = False
        if self.estado == 'activo':
            self.is_active = True
        else:
            self.is_active = False

        super().save(*args, **kwargs) 

    def __str__(self):
        return f"{self.username} ({self.get_role_display()}) - {self.get_estado_display()}"
    
