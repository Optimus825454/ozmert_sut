# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from werkzeug.security import check_password_hash, generate_password_hash

# Inspiration -> https://www.vitoshacademy.com/hashing-passwords-in-python/


def hash_pass(password):
    """Hash a password for storing."""
    return generate_password_hash(password)


def verify_pass(provided_password, stored_password):
    """Şifreyi doğrula"""
    return check_password_hash(stored_password, provided_password)
