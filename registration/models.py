from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

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
    tipo_docente = models.CharField(max_length=20, choices=TIPO_DOCENTE_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


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
    institucion_pais = models.CharField(max_length=255)  # 🔹 Un solo campo para institución y país
    anio_obtencion = models.IntegerField()
    cedula_profesional = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.get_nivel_display()}"
    
# Tabla Nombre del Profesor
class NombreProfesor(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="nombre_profesor")
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"
    
    