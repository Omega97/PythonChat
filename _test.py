import hashlib


def get_hash(s: str):
    h = hashlib.new('sha256')
    h.update(s.encode('utf-8'))
    return h.hexdigest()
