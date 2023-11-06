import bcrypt
import base64
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random


def hash_bcrypt(unhashed):
    # return bcrypt hash of the user pin/passsword
    hashed = unhashed.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(hashed, salt)
    hashed = str(hashed)[2:-1]
    return hashed


def check_pin(pin_to_check, hash_pin):
    # Check if the given pin matches the stored pin.
    pwd_to_check = pin_to_check.encode("utf-8")
    hash_pin = hash_pin.encode("utf-8")

    if bcrypt.checkpw(pwd_to_check, hash_pin):
        return True
    else:
        return False


def encrypt_password(key, password, encode=True):
    # encrypt password according to AES algorithm

    key_bytes = key.encode("utf-8")  # Encode the key as bytes
    password_bytes = password.encode("utf-8")  # Encode the password as bytes

    key = SHA256.new(
        key_bytes
    ).digest()  # Use SHA-256 over our key to get a proper-sized AES key
    IV = Random.new().read(AES.block_size)  # Generate IV
    encryptor = AES.new(key, AES.MODE_CBC, IV)

    padding = (
        AES.block_size - len(password_bytes) % AES.block_size
    )  # Calculate needed padding
    password_bytes += bytes([padding]) * padding  # Add padding bytes

    data = IV + encryptor.encrypt(
        password_bytes
    )  # Store the IV at the beginning and encrypt

    return base64.b64encode(data).decode("latin-1") if encode else data


def decrypt_password(key, source, decode=True):
    # decrypt password according to AES algorithm

    if decode:
        source = base64.b64decode(source.encode("latin-1"))

    # Convert the key to bytes
    key = key.encode("utf-8")

    key = SHA256.new(
        key
    ).digest()  # Use SHA-256 over our key to get a proper-sized AES key
    IV = source[: AES.block_size]  # Extract the IV from the beginning
    decryptor = AES.new(key, AES.MODE_CBC, IV)

    data = decryptor.decrypt(source[AES.block_size :])  # Decrypt

    padding = data[-1]  # Pick the padding value from the end
    if data[-padding:] != bytes([padding]) * padding:
        raise ValueError("Invalid padding...")

    return data[:-padding].decode("utf-8")  # Remove the padding
