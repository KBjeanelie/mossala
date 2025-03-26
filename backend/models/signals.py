from django.db.models.signals import post_delete
from django.dispatch import receiver
from backend.models.manager_profil import UserRealisation
from backend.models.project_manager import Project, ProjectImage

@receiver(post_delete, sender=UserRealisation)
def delete_realisation_image(sender, instance, **kwargs):
    """
    Supprime l'image associée à une réalisation lorsqu'elle est supprimée.
    """
    if instance.image:
        instance.image.delete(save=False)


@receiver(post_delete, sender=Project)
def delete_project_images(sender, instance, **kwargs):
    """
    Supprime toutes les images associées à un projet lorsqu'il est supprimé.
    """
    images = instance.images.all()
    for image in images:
        image.image.delete(save=False)  # Supprime le fichier image
        image.delete()  # Supprime l'objet ProjectImage