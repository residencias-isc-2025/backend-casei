from rest_framework import serializers
from actividad.models import Actividad

class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields = [
            'id',
            'clase',
            'titulo',
            'descripcion',
            'formato',
            # 'calificaciones',  ← 🔒 comentar o eliminar por ahora
            'alumno_alto', 'alumno_alto_calificacion', 'alumno_alto_evidencia',
            'alumno_promedio', 'alumno_promedio_calificacion', 'alumno_promedio_evidencia',
            'alumno_bajo', 'alumno_bajo_calificacion', 'alumno_bajo_evidencia',
        ]