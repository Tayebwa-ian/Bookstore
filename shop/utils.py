from django.utils.crypto import get_random_string
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile


def create_ref():
    """generating reference numbers for orders

    returns:
        a string unique string of 20 characters
    """
    return "Order-Ref: "+ get_random_string(20)


def generate_photo_file(self):
    """generating Images used in testing

    returns:
        returns a file to be uploaded
    """
    file = BytesIO()
    image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
    image.save(file, 'png')
    file.name = 'test.png'
    file.seek(0)
    return file