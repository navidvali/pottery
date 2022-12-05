import os
from django.core.exceptions import ValidationError


def validate_file_extension(file):
    print("==========================================validate_file_extension1")
    ext = os.path.splitext(file.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png']
    if not ext.lower() in valid_extensions:
        print("==========================================validate_file_extension2")
        return False
    else:
        return True
