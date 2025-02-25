from django.db import models
from authentication.models import User
from backend.models.domain_manager import Specialty

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nom du projet')
    description = models.TextField(verbose_name='Description')
    start_date = models.DateField(verbose_name='Date de début')
    end_date = models.DateField(null=True, blank=True, verbose_name='Date de fin')
    status = models.CharField(max_length=50, choices=[('ongoing', 'En cours'), ('completed', 'Terminé')], verbose_name='Statut')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects', verbose_name='Propriétaire')
    specialty = models.ManyToManyField(Specialty, verbose_name='Profil recherché', blank=True)
    assigned_freelancer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_projects', verbose_name='Freelance attribué')
    is_closed = models.BooleanField(default=False, verbose_name='Clôturé')
    
    def __str__(self):
        return self.name
    
    def close_project(self):
        self.is_closed = True
        self.save()

    class Meta:
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
        ordering = ['-start_date']

class ApplyProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='Utilisateur')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications', verbose_name='Projet')
    application_date = models.DateField(auto_now_add=True, verbose_name='Date de candidature')
    status = models.CharField(max_length=50, choices=[('pending', 'En attente'), ('accepted', 'Accepté'), ('rejected', 'Rejeté')], verbose_name='Statut')

    def __str__(self):
        return f"{self.user} - {self.project}"

    class Meta:
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
        ordering = ['-application_date']

class ProjectEvaluation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='evaluations', verbose_name='Utilisateur')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='evaluations', verbose_name='Projet')
    rating = models.IntegerField(verbose_name='Note')
    comments = models.TextField(verbose_name='Commentaires')
    evaluation_date = models.DateField(auto_now_add=True, verbose_name='Date d\'évaluation')

    def __str__(self):
        return f"{self.user} - {self.project} - {self.rating}"

    class Meta:
        verbose_name = 'Évaluation de projet'
        verbose_name_plural = 'Évaluations de projet'
        ordering = ['-evaluation_date']