import pytesseract as tess
tess.pytesseract.tesseract_cmd = r'D:\\Tesseract-OCR\\tesseract.exe'
from PIL  import Image
from document import models

def set_image_line(new_image):
    '''
        Enregistrer le texte de l'image sous forme de ligne
    '''
    img = Image.open(new_image.image)
    text = tess.image_to_string(img)
    lines = text.split('.')
    for i, line in enumerate(lines):
        nl = models.Transcription(
            image=new_image,
            contente=line,
            line_number = i+1
        )
        nl.save()
