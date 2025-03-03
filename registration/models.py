from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings

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

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    apellido_materno = models.CharField(max_length=100, blank=True, null=True)
    apellido_paterno = models.CharField(max_length=100, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    tipo_docente = models.CharField(max_length=20, choices=TIPO_DOCENTE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.username} {self.apellido_materno} {self.apellido_paterno} {self.nombre} {self.fecha_nacimiento} ({self.get_role_display()})"


    objects = CustomUserManager()

    def save(self, *args, **kwargs):
        """Otorga privilegios de staff a los superusuarios automáticamente"""
        if self.role == 'superuser':  # Si el usuario es Super Usuario
            self.is_staff = True
            self.is_superuser = True  # También darle permisos de superusuario
        elif self.role == 'admin':  # Si es Administrador
            self.is_staff = True
            self.is_superuser = False  # Un admin puede tener staff, pero no superuser
        else:  # Si es un usuario normal (Docente)
            self.is_staff = False
            self.is_superuser = False

        super().save(*args, **kwargs) 
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

# Tabla Formacion Academica
class FormacionAcademica(models.Model):
    NIVEL_CHOICES = [
        ('L', 'Licenciatura'),
        ('E', 'Especialidad'),
        ('M', 'Maestría'),
        ('D', 'Doctorado'),
    ]

    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="formacion_academica")
    nivel = models.CharField(max_length=1, choices=NIVEL_CHOICES)  # Solo valores L, E, M, D
    nombre = models.CharField(max_length=255)
    institucion_pais = models.ForeignKey(
        'registration.InstitucionPais',  # Corregido para evitar importación circular
        on_delete=models.CASCADE,
        related_name='formaciones_academicas',
        null=True,
        blank=True
    )
    anio_obtencion = models.IntegerField()
    cedula_profesional = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_nivel_display()}"
    
# Institucion y Pais\

class InstitucionPais(models.Model):
    nombre_institucion = models.CharField(max_length=255)
    pais = models.CharField(max_length=100)

    def ___str___(self):
        return f"{self.nombre_institucion} - {self.pais}"

# Capacitacion Docente

class CapacitacionDocente(models.Model):
    tipo_capacitacion = models.CharField(max_length=255)
    institucion_pais = models.ForeignKey(
        InstitucionPais, 
        on_delete=models.CASCADE, 
        related_name='capacitaciones',
        null=True, 
        blank=True
    )
    año_obtencion = models.PositiveIntegerField()
    horas = models.PositiveIntegerField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='capacitaciones_docentes')

    def ___str___(self):
        return f"{self.tipo_capacitacion} - {self.usuario.username}"
    
# Actualizacion Diciplinaria

class ActualizacionDisciplinaria(models.Model):
    tipo_actualizacion = models.CharField(max_length=255)
    institucion_pais = models.ForeignKey(
        'registration.InstitucionPais', 
        on_delete=models.CASCADE, 
        related_name='actualizaciones_disciplinarias',
        null=True, 
        blank=True
    )
    año_obtencion = models.PositiveIntegerField()
    horas = models.PositiveIntegerField()
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='actualizacion_disciplinar')

    def __str__(self):
        return f"{self.tipo_actualizacion} - {self.usuario.username}"
    
class GestionAcademica(models.Model):
    actividad_puesto = models.CharField(max_length=255)
    institucion_pais = models.ForeignKey(
        'registration.InstitucionPais', 
        on_delete=models.CASCADE, 
        related_name='gestion_academica',
        null=True, 
        blank=True
    )
    d_mes_año = models.DateField()
    a_mes_año = models.DateField()
    usuario = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.actividad_puesto} en {self.institucion_pais}"

class ProductosAcademicosRelevantes(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    descripcion_producto_academico = models.TextField()

    def __str__(self):
        return f"{self.usuario.username} - Producto Académico"

class ExperienciaProfesionalNoAcademica(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    actividad_puesto = models.CharField(max_length=255)
    organizacion_empresa = models.CharField(max_length=255)
    d_mes_año = models.DateField()
    a_mes_año = models.DateField()

    def ___str___(self):
        return f"{self.usuario.username} - {self.actividad_puesto}"

class ExperienciaDiseñoIngenieril(models.Model):
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