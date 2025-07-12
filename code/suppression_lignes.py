import os
import argparse
from PIL import Image

def supprimer_lignes_bas(dossier, lignes_a_supprimer=10):
    for nom_fichier in os.listdir(dossier):
        if nom_fichier.lower().endswith(".tiff"):
            chemin_complet = os.path.join(dossier, nom_fichier)
            try:
                with Image.open(chemin_complet) as img:
                    largeur, hauteur = img.size

                    if hauteur <= lignes_a_supprimer:
                        print(f"[IGNORÉ] {nom_fichier} est trop petite ({hauteur}px).")
                        continue

                    image_rognée = img.crop((0, 0, largeur, hauteur - lignes_a_supprimer))
                    image_rognée.save(chemin_complet)
                    print(f"[OK] {nom_fichier} modifiée.")
            except Exception as e:
                print(f"[ERREUR] {nom_fichier} : {e}")

def main():
    parser = argparse.ArgumentParser(description="Supprimer les 10 dernières lignes de pixels des images .tiff d'un dossier.")
    parser.add_argument("dossier", type=str, help="Chemin du dossier contenant les images .tiff")
    parser.add_argument("--lignes", type=int, default=10, help="Nombre de lignes à supprimer depuis le bas (défaut: 10)")

    args = parser.parse_args()
    if not os.path.isdir(args.dossier):
        print(f"Erreur : Le chemin '{args.dossier}' n'est pas un dossier valide.")
        return

    supprimer_lignes_bas(args.dossier, args.lignes)

if __name__ == "__main__":
    main()
