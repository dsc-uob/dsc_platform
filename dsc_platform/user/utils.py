def not_valid_username(username):
    """Check if username is valid."""
    if not username:
        return True
    if '@' in username:
        return True
    return False
