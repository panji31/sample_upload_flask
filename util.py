import hashlib

def generate_name(text):
    hash = hashlib.md5(text.encode())
    name_file_hash = hash.hexdigest()
    return name_file_hash