from django.db import models
from authentication.models import User


class WarningFromUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur')
    warning_message = models.TextField(verbose_name='Message de prévention')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    def __str__(self):
        return f"{self.user} - {self.created_at}"
    
    class Meta:
        verbose_name = 'Avertissement de l\'utilisateur'
        verbose_name_plural = 'Avertissements des utilisateurs'
        ordering = ['-created_at']


class FeedBackFromUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Utilisateur')
    feedback_message = models.TextField(verbose_name='Message de feedback')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Créé le')
    def __str__(self):
        return f"{self.user} - {self.created_at}"
    
    class Meta:
        verbose_name = 'Commentaire de l\'utilisateur'
        verbose_name_plural = 'Commentaires des utilisateurs'
        ordering = ['-created_at']