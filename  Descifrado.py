import numpy as np

def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean(b % a, a)
        return gcd, y - (b // a) * x, x

def gauss_jacques(K, m):
    det_K = int(np.round(np.linalg.det(K)))  # Calcular el determinante de la matriz de clave
    if det_K <= 0:
        raise ValueError("Error. El determinante de la matriz debe ser positivo.")

    gcd_det_m = np.gcd(det_K, m)  # Calcular el máximo común divisor entre el determinante y m
    if gcd_det_m != 1:
        raise ValueError("Error. El determinante de la matriz no es coprimo con m.")

    rows, cols = K.shape
    K = np.hstack((K, np.eye(rows, cols)))

    for i in range(rows):
        pivot = K[i, i]

        if pivot == 0:
            for k in range(i + 1, rows):
                if K[k, i] != 0:
                    K[[i, k]] = K[[k, i]]  # Swap rows i and k
                    break

        pivot = K[i, i]

        gcd, x, _ = extended_euclidean(pivot, m)

        K[i, :] = np.mod(K[i, :] * x, m)

        for j in range(rows):
            if i != j:
                K[j, :] = np.mod(K[i, :] * (-K[j, i]) + K[j, :], m)

    InvMod = K[:, cols:]
    I = K[:, :cols]

    return InvMod, I

def numbers_to_text(numbers):
    return ''.join(chr(int(num) + ord('a')) for num in numbers)  # Convertir el número a entero antes de sumarlo

def decrypt(cipher_blocks, InvMod, m):
    n = InvMod.shape[0]
    plain_blocks = [np.dot(np.array(cipher_blocks[i:i+n]), InvMod) % m for i in range(0, len(cipher_blocks), n)]
    plain_numbers = [num for block in plain_blocks for num in block]
    return numbers_to_text(map(int, plain_numbers))  # Convertir los números a enteros antes de pasarlos a la función de conversión

if __name__ == "__main__":
    K_str = input("Ingrese la matriz de clave utilizada en el cifrado (separada por comas y entre corchetes, por ejemplo: [[1,2],[3,4]]): ")
    K = np.array(eval(K_str))  # Convertir la cadena de entrada en una matriz numpy
    m = int(input("Ingrese el módulo utilizado en el cifrado: "))
    mensaje_encriptado_str = input("Ingrese el mensaje encriptado que se va a descifrar (en el formato [19, 2, 19, 2]): ")
    mensaje_encriptado = eval(mensaje_encriptado_str)  # Convertir la cadena de entrada en una lista de números

    # Obtener la matriz inversa modular
    InvMod, _ = gauss_jacques(K, m)

    # Desencriptar el mensaje encriptado
    mensaje_desencriptado = decrypt(mensaje_encriptado, InvMod, m)

    print("Matriz de clave utilizada en el cifrado:", K)
    print("Módulo utilizado en el cifrado:", m)
    print("Mensaje encriptado que se va a descifrar:", mensaje_encriptado)
    print("Mensaje desencriptado:", mensaje_desencriptado)