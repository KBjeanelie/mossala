import re

def is_valid_phone_number(phone):
    """
    Vérifie si un numéro de téléphone est valide (format international ou national).
    
    Args:
        phone (str): Le numéro de téléphone à vérifier.
    
    Returns:
        bool: True si valide, False sinon.
    """
    # Format international (+225123456789)
    pattern_international = re.compile(r"^\+\d{1,3}\d{6,14}$")
    
    # Format national (ex: 07 12 34 56 78 pour la Côte d'Ivoire)
    pattern_national = re.compile(r"^\d{8,10}$")  # À adapter selon le pays
    
    return bool(pattern_international.match(phone) or pattern_national.match(phone))
