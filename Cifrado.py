import numpy as np

def text_to_numbers(text):
    return [ord(char) - ord('a') for char in text.lower() if char.isalpha()]

def encrypt(text, K, m):
    numbers = text_to_numbers(text)
    n = K.shape[0]
    # Fill with zeros if the length is not a multiple of n
    remainder = len(numbers) % n
    if remainder:
        numbers.extend([0] * (n - remainder))
    blocks = [numbers[i:i+n] for i in range(0, len(numbers), n)]

    cipher_blocks = []
    for block in blocks:
        block = np.array(block)
        cipher_block = np.dot(block, K) % m
        cipher_blocks.extend(cipher_block.tolist())  # Convert numpy array to list
    return cipher_blocks

# Gauss-Jacques method to obtain modular inverse matrices variable sized without a theoretical limit.
# This method is efficient computationally and applicable in symmetric cryptography.
# It also discusses some phenomena in linear arithmetic spaces and related theorems.

# Function to calculate the modular inverse of a matrix using Gauss-Jacques method
def modular_inverse(matrix, modulus):
    # Calculate the determinant of the matrix modulo modulus
    determinant = int(round(np.linalg.det(matrix))) % modulus
    # Calculate the modular inverse of the determinant using the extended Euclidean algorithm
    _, determinant_inverse, _ = extended_euclidean(determinant, modulus)
    # Calculate the adjugate matrix (transpose of the cofactor matrix)
    adjugate = (determinant * np.linalg.inv(matrix)).astype(int) % modulus
    # Multiply each element of the adjugate matrix by the determinant inverse modulo modulus
    inverse_matrix = (adjugate * determinant_inverse) % modulus
    return inverse_matrix

# Extended Euclidean algorithm to calculate the multiplicative inverse of a number modulo modulus
def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = extended_euclidean(b % a, a)
        return gcd, y - (b // a) * x, x

if __name__ == "__main__":
    np.random.seed(0)
    n = 2  # Size of the key matrix
    K = np.random.randint(1, 10, size=(n, n))  # Generate a random key matrix
    m = 29  # Modulus -> a prime number

    original_message = input("Enter the message to encrypt: ")  # Message to encrypt

    # Encrypt the message
    encrypted_message = encrypt(original_message, K, m)

    print("Original message:", original_message)
    print("Encrypted message:", encrypted_message)
    print("Key matrix K:")
    for row in K:
        print("[{}]".format(','.join(map(str, row))), end="\n,")
    print("Modulus m:", m)

    