from django.db import models
from authentication.models import User

class UserExperience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    title = models.CharField(max_length=255, verbose_name='Titre')
    company = models.CharField(max_length=255, verbose_name='Entreprise')
    start_date = models.DateField(verbose_name='Date de début')
    end_date = models.DateField(null=True, blank=True, verbose_name='Date de fin')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return f"{self.title} at {self.company}"
    
    class Meta:
        verbose_name = 'Expérience'
        verbose_name_plural = 'Expériences'
        ordering = ['-start_date']


class UserEducation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    institution = models.CharField(max_length=255, verbose_name='Institution')
    degree = models.CharField(max_length=255, verbose_name='Diplôme')
    field_of_study = models.CharField(max_length=255, verbose_name='Domaine d\'étude')
    start_date = models.DateField(verbose_name='Date de début')
    end_date = models.DateField(null=True, blank=True, verbose_name='Date de fin')
    description = models.TextField(verbose_name='Description')

    def __str__(self):
        return f"{self.degree} in {self.field_of_study} from {self.institution}"
    
    class Meta:
        verbose_name = 'Formation'
        verbose_name_plural = 'Formations'
        ordering = ['-start_date']


class UserLanguage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='languages')
    language = models.CharField(max_length=255, verbose_name='Langue')
    proficiency = models.CharField(max_length=255, verbose_name='Niveau de maîtrise')

    def __str__(self):
        return f"{self.language} ({self.proficiency})"
    
    class Meta:
        verbose_name = 'Langue'
        verbose_name_plural = 'Langues'
        ordering = ['language']


class UserPortfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolios')
    project_name = models.CharField(max_length=255, verbose_name='Nom du projet')
    description = models.TextField(verbose_name='Description')
    link = models.URLField(verbose_name='Lien du projet', null=True, blank=True)
    date = models.DateField(verbose_name='Date du projet')

    def __str__(self):
        return self.project_name
    
    class Meta:
        verbose_name = 'Portfolio'
        verbose_name_plural = 'Portfolios'
        ordering = ['-date']

class UserRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    recommender_name = models.CharField(max_length=255, verbose_name='Nom du recommandant')
    recommender_position = models.CharField(max_length=255, verbose_name='Poste du recommandant')
    recommender_company = models.CharField(max_length=255, verbose_name='Entreprise du recommandant')
    recommendation = models.TextField(verbose_name='Recommandation')
    date = models.DateField(verbose_name='Date de la recommandation')

    def __str__(self):
        return f"Recommendation by {self.recommender_name}"
    
    class Meta:
        verbose_name = 'Recommendation'
        verbose_name_plural = 'Recommendations'
        ordering = ['-date']


class UserRealisation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='realisations')
    realisation_name = models.CharField(max_length=255, verbose_name='Nom de la réalisation')
    description = models.TextField(verbose_name='Description')
    date = models.DateField(verbose_name='Date de la réalisation')
    image = models.ImageField(upload_to='realisation_images/', verbose_name='Image')
    
    def __str__(self):
        return self.realisation_name
    
    class Meta:
        verbose_name = 'Réalisation'
        verbose_name_plural = 'Réalisations'
        ordering = ['-date']