from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
 
 
def encrypt_image(image_path: str, key: bytes) -> bytes:
    """
    Encripta una imagen usando el algoritmo de encriptacion AES.
 
    Parametros:
    - image_path: str
        Ruta de la imagen.
    - key: bytes
        La clave de encriptacion.
 
    Regresa:
    - bytes
        La imagen encriptada.
 
    Lanza error:
    - FileNotFoundError:
         Si la imagen no se encontro
    """
 
    # Lee la imagen
    try:
        with open(image_path, 'rb') as file:
            image_data = file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file '{image_path}' not found.")
 
    # Genera un vector de inicializacion aleatorio
    iv = get_random_bytes(AES.block_size)
 
    # Crea un objeto de cifrado con AES usando la llave privada
    cipher = AES.new(key, AES.MODE_CBC, iv)
 
    #  Rellenar los datos de la imagen para que cumple con el tamaño del bloque
    padded_image_data = pad(image_data, AES.block_size)
 
    # Encriptar los datos de la imagen
    encrypted_image_data = cipher.encrypt(padded_image_data)
 
    # Agregar el vector de inicializacion a los datos de la imagen encryptada
    encrypted_image_data_with_iv = iv + encrypted_image_data
 
    return encrypted_image_data_with_iv
 
 
def decrypt_image(encrypted_image_data: bytes, key: bytes) -> bytes:
    """

    Desencripta una imagen encriptada usando el algoritmo AES.
 
    Parametros:
    - encrypted_image_data: bytes
        Los datos de la imagen encriptada.
    - key: bytes
        La llave de encriptacion
 
    Regresa:
    - bytes
        Los datos de la imagen desencriptada.
 
    Lanza error:
    - ValueError:
        Si la longitud de la imagen encriptada es invalida
    """
 
    # Vertificar la longitud de los datos de la imagen encriptada
    if len(encrypted_image_data) < AES.block_size:
        raise ValueError("Invalid length of encrypted image data.")
 
    # Extraer el vector de inicializacion
    iv = encrypted_image_data[:AES.block_size]
 
    # Crear un objeto de cifrado AES con la llave provisionada y el vector de inicialización extraído 
    cipher = AES.new(key, AES.MODE_CBC, iv)
 
    # Desencriptar los datos de imagen
    decrypted_image_data = cipher.decrypt(encrypted_image_data[AES.block_size:])
 
    # Eliminar los datos adicionados a la imagen
    unpadded_image_data = unpad(decrypted_image_data, AES.block_size)
 
    return unpadded_image_data
 
 
# Solicitar al usuario iamgen y clave

image_path = input("Ingresa la ruta de la imagen: ")
while len(image_path) == 0:
    print("Debes ingresar una ruta válida")
    image_path = input("Ingresa la ruta de la imagen: ")

encryption_key =  input("Ingresa una clave de encriptación de 16 caracteres: ")
while len(encryption_key) != 16:
    print("Debes ingresar una clave de 16 carateres")
    encryption_key = input("Ingresa una clave de encriptación: ")
encryption_bytes = bytes(encryption_key, 'utf-8')

# Encriptar imagen
encrypted_image_data = encrypt_image(image_path, encryption_bytes)

encrypted_image_path = "./encrypted_image.jpg"
with open(encrypted_image_path, 'wb') as file:
    file.write(encrypted_image_data)
 
# Desencriptar imagen
decrypted_image_data = decrypt_image(encrypted_image_data, encryption_bytes)
 
# Guardar la imagen en un nuevo archivo
decrypted_image_path = "./decrypted_image.jpg"
with open(decrypted_image_path, 'wb') as file:
    file.write(decrypted_image_data)