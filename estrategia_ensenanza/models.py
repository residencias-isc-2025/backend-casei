from django.db import models

# Create your models here.
class EstrategiaEnsenanza(models.Model):
    descripcion = models.TextField()

    def ___str___(self):
        return self.descripcion[:30]