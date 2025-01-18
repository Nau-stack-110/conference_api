import qrcode
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os
from django.conf import settings
import uuid

class TicketGenerator:
    def __init__(self, registration):
        self.registration = registration
        self.conference = registration.session.conference
        self.session = registration.session
        self.user = registration.user
        self.unique_code = str(uuid.uuid4()) 
        
    def generate_qr_code(self):
        # Créer les données pour le QR code
        qr_data = (
            f"Conférence: {self.conference.title}\n"
            f"Session: {self.session.title}\n"
            f"Date: {self.session.start_time.strftime('%d/%m/%Y %H:%M')}\n"
            f"Participant: {self.user.username}\n"
            f"Code Unique: {self.unique_code}\n"
        )
        
        # Générer le QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Créer l'image QR
        qr_image = qr.make_image(fill_color="black", back_color="white").convert("RGBA")  # Convertir en RGBA
        
        # Ajouter le logo
        logo_path = os.path.join(settings.BASE_DIR, 'Linux.png')  # Chemin vers le logo
        logo = Image.open(logo_path).convert("RGBA")  # Convertir le logo en RGBA
        logo = logo.resize((40, 40))  # Redimensionner le logo
        
        # Ajouter le logo au QR code
        qr_image.paste(logo, (qr_image.size[0] // 2 - logo.size[0] // 2, qr_image.size[1] // 2 - logo.size[1] // 2), logo)
        
        # Sauvegarder temporairement l'image
        qr_buffer = BytesIO()
        qr_image.save(qr_buffer, format='PNG')
        qr_buffer.seek(0)
        
        return qr_buffer
    
    def generate_ticket(self):
        # Créer un buffer pour le ticket
        ticket_width = 600
        ticket_height = 400
        
        # Créer une image blanche pour le ticket
        ticket_image = Image.new('RGB', (ticket_width, ticket_height), 'white')
        draw = ImageDraw.Draw(ticket_image)
        
        # Ajouter le titre
        title_font = ImageFont.load_default()
        draw.text((20, 20), "Ticket de Conférence", fill="black", font=title_font)
        
        # Ajouter les informations
        info_list = [
            f"Conférence: {self.conference.title}",
            f"Session: {self.session.title}",
            f"Date: {self.session.start_time.strftime('%d/%m/%Y %H:%M')}",
            f"Participant: {self.user.username}",
            f"Code Unique: {self.unique_code}"
        ]
        
        y_position = 60
        for info in info_list:
            draw.text((20, y_position), info, fill="black", font=title_font)
            y_position += 20
        
        # Ajouter le QR code
        qr_buffer = self.generate_qr_code()
        qr_image = Image.open(qr_buffer)
        qr_image = qr_image.resize((100, 100))  # Redimensionner le QR code
        ticket_image.paste(qr_image, (20, y_position))  # Ajouter le QR code à l'image
        
        # Générer un nom de fichier unique
        filename = f"ticket_{uuid.uuid4().hex[:8]}.png"
        
        # Créer le dossier tickets s'il n'existe pas
        tickets_dir = os.path.join(settings.MEDIA_ROOT, 'tickets')
        if not os.path.exists(tickets_dir):
            os.makedirs(tickets_dir)
        
        # Sauvegarder le ticket
        file_path = os.path.join(tickets_dir, filename)
        ticket_image.save(file_path)
        
        return f'tickets/{filename}' 