import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mossala.settings')  # Remplace 'ton_projet' par le nom de ton projet Django
django.setup()

from backend.models.domain_manager import Domain, Specialty, Job  # Remplace 'app' par le nom de ton application Django

data = [
    {
        "domain": "Informatique",
        "specialties": [
            {"name": "Développement Web", "jobs": ["Développeur Frontend", "Développeur Backend", "Développeur Full Stack"]},
            {"name": "Développement Mobile", "jobs": ["Développeur Android", "Développeur iOS", "Développeur Flutter", "Développeur React Native"]},
            {"name": "Cybersécurité", "jobs": ["Analyste en sécurité", "Pentester", "Ingénieur SOC"]},
            {"name": "Data Science", "jobs": ["Data Analyst", "Data Engineer", "Data Scientist"]},
            {"name": "Cloud Computing", "jobs": ["Ingénieur DevOps", "Architecte Cloud"]},
            {"name": "Intelligence Artificielle", "jobs": ["Ingénieur IA", "Spécialiste en Machine Learning"]},
            {"name": "Réseaux et Systèmes", "jobs": ["Administrateur Système", "Ingénieur Réseau"]},
        ],
    },
    {
        "domain": "Bâtiment et Travaux Publics (BTP)",
        "specialties": [
            {"name": "Construction", "jobs": ["Maçon", "Charpentier", "Chef de chantier", "Aide Maçon"]},
            {"name": "Génie Civil", "jobs": ["Ingénieur Génie Civil", "Conducteur de travaux"]},
            {"name": "Électricité", "jobs": ["Électricien du bâtiment", "Technicien en énergie renouvelable"]},
            {"name": "Plomberie", "jobs": ["Plombier", "Installateur sanitaire"]},
            {"name": "Architecture", "jobs": ["Architecte", "Dessinateur en bâtiment"]},
        ],
    },
    {
        "domain": "Médecine et Santé",
        "specialties": [
            {"name": "Médecine Générale", "jobs": ["Médecin généraliste", "Infirmier", "Pharmacien"]},
            {"name": "Médecine Spécialisée", "jobs": ["Cardiologue", "Dentiste", "Ophtalmologue"]},
            {"name": "Chirurgie", "jobs": ["Chirurgien général", "Neurochirurgien"]},
            {"name": "Médecine Alternative", "jobs": ["Chiropracteur", "Naturopathe"]},
            {"name": "Paramédical", "jobs": ["Kinésithérapeute", "Orthophoniste"]},
        ],
    },
    {
        "domain": "Commerce et Marketing",
        "specialties": [
            {"name": "Vente", "jobs": ["Vendeur", "Responsable Commercial"]},
            {"name": "Marketing Digital", "jobs": ["Community Manager", "SEO Manager", "Growth Hacker"]},
            {"name": "Gestion et Finance", "jobs": ["Comptable", "Analyste Financier", "Contrôleur de Gestion"]},
        ],
    },
    {
        "domain": "Agriculture",
        "specialties": [
            {"name": "Agriculture Biologique", "jobs": ["Agriculteur Bio", "Expert en permaculture"]},
            {"name": "Élevage", "jobs": ["Éleveur Bovin", "Éleveur Avicole"]},
            {"name": "Pêche et Aquaculture", "jobs": ["Pêcheur", "Technicien en aquaculture"]},
        ],
    },
    {
        "domain": "Transport et Logistique",
        "specialties": [
            {"name": "Logistique", "jobs": ["Gestionnaire de stock", "Magasinier"]},
            {"name": "Transport Routier", "jobs": ["Chauffeur poids lourd", "Conducteur VTC"]},
        ],
    },
    {
        "domain": "Art et Culture",
        "specialties": [
            {"name": "Musique", "jobs": ["Chanteur", "Producteur Musical"]},
            {"name": "Cinéma", "jobs": ["Réalisateur", "Monteur Vidéo"]},
            {"name": "Design Graphique", "jobs": ["Graphiste", "Illustrateur"]},
        ],
    },
    {
        "domain": "Éducation et Formation",
        "specialties": [
            {"name": "Enseignement", "jobs": ["Professeur des écoles", "Enseignant en lycée"]},
            {"name": "Formation Professionnelle", "jobs": ["Formateur en informatique", "Coach en développement personnel"]},
        ],
    },
    {
        "domain": "Énergie et Environnement",
        "specialties": [
            {"name": "Énergies Renouvelables", "jobs": ["Ingénieur en énergies renouvelables", "Technicien solaire"]},
            {"name": "Gestion des Déchets", "jobs": ["Agent de tri", "Spécialiste du recyclage"]},
        ],
    },
    {
        "domain": "Sécurité et Défense",
        "specialties": [
            {"name": "Sécurité Publique", "jobs": ["Policier", "Gendarme"]},
            {"name": "Sécurité Privée", "jobs": ["Agent de sécurité", "Gardien de nuit"]},
        ],
    },
]

def insert_data():
    for domain_data in data:
        domain, created = Domain.objects.get_or_create(name=domain_data["domain"])
        
        for specialty_data in domain_data["specialties"]:
            specialty, created = Specialty.objects.get_or_create(name=specialty_data["name"], domain=domain)

            for job_name in specialty_data["jobs"]:
                Job.objects.get_or_create(title=job_name, specialty=specialty)
    
    print("✅ Données insérées avec succès !")

if __name__ == "__main__":
    insert_data()
