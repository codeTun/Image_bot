import os
import requests
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from dotenv import load_dotenv

output_width = 35.5
output_height = 55.5

load_dotenv('.env')
# Chemin du dossier contenant les images d'entrée
input_folder = "C:/Users/ihebl/OneDrive/Bureau/Job"

# Création du dossier de sortie s'il n'existe pas
output_folder = "//Path"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Chemin complet du fichier PDF de sortie
output_pdf_path = os.path.join(output_folder, "output.pdf")

# Parcours des fichiers dans le dossier d'entrée
image_files = [filename for filename in os.listdir(input_folder) if os.path.isfile(os.path.join(input_folder, filename))]
image_files.sort()

# Récupération du token d'API à partir de l'environnement
api_token = os.getenv("API KEY")

# Vérification si le token d'API est défini
if api_token is None:
    print("Le token d'API n'est pas défini.")
    exit()

# Création du PDF avec ReportLab
c = canvas.Canvas(output_pdf_path, pagesize=letter)

# Fonction pour améliorer la qualité de l'image via l'API d'IA
def enhance_image(image):
    # Appel à l'API pour améliorer la qualité de l'image
    api_endpoint = "API URL "  # Remplacez par l'URL de votre API d'amélioration d'image

    headers = {
        "Authorization": f"Bearer {api_token}"
    }

    # Conversion de l'image en bytes
    image_bytes = image.tobytes()

    response = requests.post(api_endpoint, data=image_bytes, headers=headers)

    # Vérification de la réponse de l'API et récupération de l'image améliorée
    if response.status_code == 200:
        enhanced_image_bytes = response.content
        enhanced_image = Image.frombytes("RGB", image.size, enhanced_image_bytes)
        return enhanced_image
    else:
        print("Erreur lors de l'appel à l'API pour l'amélioration de l'image.")
        return None
    
for image_file in image_files:
    # Chemin complet du fichier d'entrée
    input_path = os.path.join(input_folder, image_file)

    # Vérification si le fichier est une image
    if image_file.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
        # Chargement de l'image avec Pillow
        image = Image.open(input_path)

        # Amélioration de la qualité de l'image avec l'API d'IA
        enhanced_image = enhance_image(image)

        if enhanced_image is not None:
            # Redimensionnement de l'image améliorée à la taille spécifiée
            resized_image = enhanced_image.resize((int(output_width), int(output_height)), Image.ANTIALIAS)

            # Chemin complet du fichier de sortie (image temporaire)
            temp_output_path = os.path.join(output_folder, f"temp_{image_file}")

            # Sauvegarde de l'image redimensionnée dans le dossier de sortie (temporairement)
            resized_image.save(temp_output_path)

            # Ajout de l'image à la page PDF avec ReportLab
            c.drawImage
