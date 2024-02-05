from django.core.exceptions import ValidationError

# file size validation
def file_size(value):
    filesize=value.size
    if filesize > 40000000: # 5 mb => 1 MB  = 8000000
        raise ValidationError("Maximum size is 5 MB")