#for QR and PDF
from django.conf import settings
import qrcode,os
from io import BytesIO
from django.core.files import File
from django.template.loader import get_template
from xhtml2pdf import pisa


def generate_qr_code(permit):
    """Generate QR code from permit_number and save to permit.qr_code"""
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    qr.add_data(permit.permit_number)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    
    file_name = f"qr_{permit.permit_number}.png"
    permit.qr_code.save(file_name, File(buffer), save=False)
    
    buffer.close()


def generate_pdf(permit):
    """Generate PDF from permit_pdf.html template and save to permit.pdf_file"""
    
    template = get_template('permits/permit_pdf.html')

    logo_path = os.path.join(settings.BASE_DIR, 'main', 'static', 'images', 'iftar_platform.png')
    
    context = {'permit': permit,'logo_path': logo_path}
    html = template.render(context)
    
    buffer = BytesIO()
    pisa.CreatePDF(html, dest=buffer)
    buffer.seek(0)
    
    file_name = f"permit_{permit.permit_number}.pdf"
    permit.pdf_file.save(file_name, File(buffer), save=False)
    
    buffer.close()