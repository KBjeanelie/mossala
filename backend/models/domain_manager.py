from django.db import models

class Domain(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Nom de domaine')
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modifié le')
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Domaine'
        verbose_name_plural = 'Domaines'
        ordering = ['name']



class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name='Spécialité')
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE, verbose_name='Domaine')
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modifié le')
    
    def __str__(self):
        return f"Spécialité : {self.name} - {self.domain}"
    
    class Meta:
        verbose_name = 'Spécialité'
        verbose_name_plural = 'Spécialités'
        ordering = ['name']


class Job(models.Model):
    title = models.CharField(max_length=255, unique=True, verbose_name='Intitulé du poste')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, verbose_name='Spécialité')
    description = models.TextField(verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Modifié le')
    
    def __str__(self):
        return f"Poste : {self.title} - {self.specialty}"
    
    class Meta:
        verbose_name = 'Poste'
        verbose_name_plural = 'Postes'
        ordering = ['title']