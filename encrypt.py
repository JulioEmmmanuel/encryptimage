from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
 
 
def encrypt_image(image_path: str, key: bytes) -> bytes:
    """
    Encrypts an image file using AES encryption algorithm.
 
    Parameters:
    - image_path: str
        The path to the image file to be encrypted.
    - key: bytes
        The encryption key to be used for AES encryption.
 
    Returns:
    - bytes
        The encrypted image data.
 
    Raises:
    - FileNotFoundError:
        If the image file specified by 'image_path' does not exist.
    """
 
    # Read the image file
    try:
        with open(image_path, 'rb') as file:
            image_data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
 
    # Generate a random initialization vector (IV)
    iv = get_random_bytes(AES.block_size)
 
    # Create an AES cipher object with the provided key and AES.MODE_CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
 
    # Pad the image data to match the AES block size
    padded_image_data = pad(image_data, AES.block_size)
 
    # Encrypt the padded image data
    encrypted_image_data = cipher.encrypt(padded_image_data)
 
    # Prepend the IV to the encrypted image data
    encrypted_image_data_with_iv = iv + encrypted_image_data
 
    return encrypted_image_data_with_iv
 
 
def decrypt_image(encrypted_image_data: bytes, key: bytes) -> bytes:
    """
    Decrypts an encrypted image using AES encryption algorithm.
 
    Parameters:
    - encrypted_image_data: bytes
        The encrypted image data.
    - key: bytes
        The encryption key used for AES encryption.
 
    Returns:
    - bytes
        The decrypted image data.
 
    Raises:
    - ValueError:
        If the length of the encrypted image data is invalid.
    """
 
    # Check if the length of the encrypted image data is valid
    if len(encrypted_image_data) < AES.block_size:
        raise ValueError("Invalid length of encrypted image data.")
 
    # Extract the IV from the encrypted image data
    iv = encrypted_image_data[:AES.block_size]
 
    # Create an AES cipher object with the provided key, AES.MODE_CBC mode, and the extracted IV
    cipher = AES.new(key, AES.MODE_CBC, iv)
 
    # Decrypt the encrypted image data (excluding the IV)
    decrypted_image_data = cipher.decrypt(encrypted_image_data[AES.block_size:])
 
    # Unpad the decrypted image data
    unpadded_image_data = unpad(decrypted_image_data, AES.block_size)
 
    return unpadded_image_data
 
 
# Usage:

image_path = input("Ingresa la ruta de la imagen")
 
# Generate a random encryption key
encryption_key =  input("Ingresa una clave de encriptación de 16 caracters")
while len(encryption_key) != 16:
    encryption_key =  input("Ingresa una clave de encriptación de 16 caracters")

encrypted_image_data = encrypt_image(image_path, encryption_key)
 
# Decrypt the encrypted image data
decrypted_image_data = decrypt_image(encrypted_image_data, encryption_key)
 
# Save the decrypted image data to a new file
decrypted_image_path = "./decrypted_image.jpg"
with open(decrypted_image_path, 'wb') as file:
    file.write(decrypted_image_data)