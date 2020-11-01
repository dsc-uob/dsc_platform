import os
import uuid


def not_valid_username(username):
    """Check if username is valid."""
    if not username:
        return True
    if '@' in username:
        return True
    return False


def image_file_path(app_name: str, instance, filename: str):
    "Generate a file path for new image."
    ext = filename.split('.')[-1]
    filename = f'{uuid.uuid4()}.{ext}'

    return os.path.join(f'uploads/{app_name}/', filename)


def user_image_file_path(instance, filename):
    """Generate a file path for new user image."""
    return image_file_path(app_name='user',
                           instance=instance, filename=filename)
