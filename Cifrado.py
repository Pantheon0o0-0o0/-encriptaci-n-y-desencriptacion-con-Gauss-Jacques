import numpy as np

def text_to_numbers(text):
    return [ord(char) - ord('a') for char in text.lower() if char.isalpha()]

def encrypt(text, K, m):
    numbers = text_to_numbers(text)
    n = K.shape[0]
    # Llenar con ceros si la longitud no es múltiplo de n 
    remainder = len(numbers) % n
    if remainder:
        numbers.extend([0] * (n - remainder))
    blocks = [numbers[i:i+n] for i in range(0, len(numbers), n)]

    cipher_blocks = []
    for block in blocks:
        block = np.array(block)
        cipher_block = np.dot(block, K) % m
        cipher_blocks.extend(cipher_block.tolist())  # Convertir el array numpy a lista
    return cipher_blocks

if __name__ == "__main__":
    np.random.seed(0)
    n = 2  # Tamaño de la matriz de clave
    K = np.random.randint(1, 10, size=(n, n))  # Generar una matriz de clave aleatoria
    m = 29  # Módulo -> un número primo

    mensaje_original = input("Ingrese el mensaje a encriptar: ")  # Mensaje a encriptar

    # Encriptar el mensaje
    mensaje_encriptado = encrypt(mensaje_original, K, m)

    print("Mensaje original:", mensaje_original)
    print("Mensaje encriptado:", mensaje_encriptado)
    print("Matriz de clave K:")
    for row in K:
        print("[{}]".format(','.join(map(str, row))),end="\n,")
    print("Módulo m:", m)