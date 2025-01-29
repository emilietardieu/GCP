from pathlib import Path

def trouver_chemin_dans_archives(chemin_original):
    """
    Recherche un chemin similaire dans les archives.

    Args:
        chemin_original (Path): Chemin source non trouvé.
        chemins_archives (list): Liste des emplacements des archives.

    Returns:
        Path ou None: Retourne le chemin trouvé ou None si aucun chemin n'est trouvé.
    """
    chemin_alternatif = Path(str(chemin_original).replace("/media/nas-production", "/media/nas-archives"))
    if chemin_alternatif.exists():
        print(f"Chemin trouvé dans les archives : {chemin_alternatif}")
        return chemin_alternatif
    else :
        print(f"Chemin introuvable dans les archives : {chemin_alternatif}")
        return None
    