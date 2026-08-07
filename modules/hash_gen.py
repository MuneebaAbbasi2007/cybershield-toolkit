import hashlib

def generate_hashes(text):
    md5_hash = hashlib.md5(text.encode()).hexdigest()
    sha1_hash = hashlib.sha1(text.encode()).hexdigest()
    sha256_hash = hashlib.sha256(text.encode()).hexdigest()

    return {
    "md5": md5_hash,
    "sha1": sha1_hash,
    "sha256": sha256_hash,
    "md5_note": "Fast but not recommended for security.",
    "sha1_note": "Weak, avoid for security purposes.",
    "sha256_note": "Recommended for modern integrity verification."
}