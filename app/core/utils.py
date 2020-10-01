def not_valid_username(username):
    """Chack if username is valid."""
    if not username:
        return True
    if '@' in username:
        return True
    return False
