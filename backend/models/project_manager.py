from django.db import models
from authentication.models import User
from backend.models.domain_manager import Specialty

class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nom du projet')
    description = models.TextField(verbose_name='Description')
    amount = models.FloatField(verbose_name='Montant', default=1000)
    adress = models.CharField(max_length=255, verbose_name='Adresse', blank=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_projects', verbose_name='Propriétaire')
    specialty = models.ManyToManyField(Specialty, verbose_name='Profil recherché', blank=True)
    assigned_freelancer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_projects', verbose_name='Freelance attribué')
    is_closed = models.BooleanField(default=False, verbose_name='Clôturé')
    created_at = models.DateField(auto_now_add=True, verbose_name='Date de début')
    def __str__(self):
        return self.name
    
    def close_project(self):
        self.is_closed = True
        self.save()

    class Meta:
        verbose_name = 'Projet'
        verbose_name_plural = 'Projets'
        ordering = ['-created_at']

class ProjectImage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images', verbose_name='Projet')
    image = models.ImageField(upload_to='project_images/', verbose_name='Image')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Date d\'ajout')

    def __str__(self):
        return f"Image for project: {self.project.name}"

    class Meta:
        verbose_name = 'Image de projet'
        verbose_name_plural = 'Images de projet'
        ordering = ['-uploaded_at']

class ApplyProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications', verbose_name='Utilisateur')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='applications', verbose_name='Projet')
    amount = models.FloatField(verbose_name='Montant', default=1000)
    duration = models.CharField(max_length=255, verbose_name='Durée', blank=True, null=True)
    description = models.TextField(verbose_name='Description', blank=True, null=True)
    application_date = models.DateField(auto_now_add=True, verbose_name='Date de candidature')

    def __str__(self):
        return f"{self.user} - {self.project}"

    class Meta:
        verbose_name = 'Candidature'
        verbose_name_plural = 'Candidatures'
        ordering = ['-application_date']

class ProjectMessage(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='messages', verbose_name='Projet')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages', verbose_name='Expéditeur')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages', verbose_name='Destinataire')
    content = models.TextField(verbose_name='Contenu du message')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Date et heure')

    def __str__(self):
        return f"Message de {self.sender} à {self.receiver} pour le projet {self.project.name}"

    class Meta:
        verbose_name = 'Message de projet'
        verbose_name_plural = 'Messages de projets'
        ordering = ['-timestamp']



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