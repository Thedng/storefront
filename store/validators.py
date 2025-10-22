from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 500000
    print(file.size)
    if file.size > max_size_kb:
        raise ValidationError(f'files can not be larger than {max_size_kb} kb')