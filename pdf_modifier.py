from PyPDF2 import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from io import BytesIO
import os

def modify_pdf(filename, cpf, position, color, upload_folder):
    packet = BytesIO()
    can = canvas.Canvas(packet, pagesize=A4)
    
    if position == 'top-left':
        x = 50
        y = 800
    elif position == 'top-right':
        x = 500
        y = 800
    elif position == 'bottom-left':
        x = 50
        y = 50
    elif position == 'bottom-right':
        x = 500
        y = 50
    else:
        raise ValueError('Posição Inválida')
    
    print(f'Desenho do CPF na posição: {x},{y}')
    
    can.setFillColor(color)
    can.setFont('Helvetica',8)
    can.drawString(x,y,cpf)
    
    can.save()
    
    try:
        packet.seek(0)
        new_pdf = PdfReader(packet)
        print('PDF criado usando CPF com sucesso')
    except Exception as e:
        print('Erro ao criar o PDF com CPF' + str(e))
    
    try:
        existing_pdf = PdfReader(open(os.path.join(upload_folder,filename), 'rb'))
        print("Sucesso em abrir o PDF.")
        output = PdfWriter()
        print(f'Número de páginas do PDF é: {len(existing_pdf.pages)}')
        
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            page.merge_page(new_pdf.pages[0])
            output.add_page(page)
        
        with open(os.path.join(upload_folder, filename), 'wb') as outputStream:
            output.write(outputStream)
            
        print(f'PDF modificado em: {os.path.join(upload_folder, filename)}')
    except Exception as e:
        print("Error ao abrir o PDF gerado: " + str(e))