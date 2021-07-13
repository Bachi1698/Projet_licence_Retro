from django.db import models


# Create your models here.
class Projet(models.Model):
    nom = models.CharField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    

    class Meta:
        verbose_name = 'projet'
        verbose_name_plural = 'projets'

    def __str__(self):
        return self.nom

class Images(models.Model):
    image = models.ImageField(upload_to='images/')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    projet = models.ForeignKey(Projet,on_delete=models.CASCADE,related_name='image_projet')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'
    
    @property
    def get_all_content(self):
        lines = [line.contente for line in self.image_transcription.all().order_by('line_number')]
        return '. '.join(lines)

    def __str__(self):
        return self.projet.nom


class Transcription(models.Model):
    image = models.ForeignKey(Images,on_delete=models.CASCADE,related_name='image_transcription')
    contente = models.TextField(null=True,blank=True)
    line_number = models.IntegerField(default=0)
    checked = models.BooleanField(default=False)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.contente


