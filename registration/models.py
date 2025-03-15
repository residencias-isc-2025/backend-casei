from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings
from usuarios.models import CustomUser
from institucion.models import InstitucionPais
from adscripcion.models import AreaAdscripcion

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
"""
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
        'registration.AreaAdscripcion', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='usuarios'
    )
    objects = CustomUserManager()

    def save(self, *args, **kwargs):

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
"""
# Tabla Formacion Academica

    
# Institucion y Pais\

# Capacitacion Docente

    
# Actualizacion Diciplinaria






class ExperienciaProfesionalNoAcademica(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actividad_puesto = models.CharField(max_length=255)
    organizacion_empresa = models.CharField(max_length=255)
    d_mes_anio = models.DateField()
    a_mes_anio = models.DateField()

    def ___str___(self):
        return f"{self.usuario.username} - {self.actividad_puesto}"

class ExperienciaDisenoIngenieril(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    organismo = models.CharField(max_length=255)
    periodo = models.IntegerField()
    nivel_experiencia = models.CharField(max_length=255)

    def ___str___(self):
        return f"{self.usuario.username} - {self.organismo}"
    
class LogrosProfesionales(models.Model):
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    descripcion = models.TextField()

    def ___str___(self):
        return f"{self.usuario.username} - {self.descripcion[:30]}..."

class Participacion(models.Model):
    organismo = models.CharField(max_length=255)
    periodo = models.IntegerField()
    nivel_p = models.CharField(max_length=255)
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.organismo} - {self.periodo}"

class Premio(models.Model):
    descripcion = models.CharField(max_length=255)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descripcion[:30]}..."
    
class Aportacion(models.Model):
    descripcion = models.CharField(max_length=255)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.descripcion[:30]}..."

"""   
class AreaAdscripcion(models.Model):
    nombre = models.CharField(max_length=255)
    siglas = models.CharField(max_length=20)

    ESTADO_CHOICES = (
        ('activo', 'Activo'),
        ('inactivo', "Inactivo"),
    )
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')

    def __str__(self):
        return f"{self.nombre} ({self.siglas})"

"""

