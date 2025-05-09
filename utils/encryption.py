import random
from ValidWords import ENGLISH_WORDS

class CaesarCipher:
    """
    A utility class for performing Caesar cipher encryption and decryption.

    The Caesar cipher is a substitution cipher that shifts the characters
    in the input text by a specified number of positions in the alphabet.
    This class provides methods for both encryption and decryption.

    Methods:
        encrypt(text: str, shift: int = None) -> str:
            Encrypts the given text using the Caesar cipher with the specified shift.
            If no shift is provided, a random shift between 1 and 26 is used.

        decrypt(text: str) -> str:
            Attempts to decrypt the given text by finding the most likely shift
            based on English word matches. This method assumes the text was
            encrypted using the Caesar cipher.
    """
    @staticmethod
    def encrypt(text: str, shift: int = None) -> str:
        """
        Args:
            text (str): The input text to be encrypted.
            shift (int, optional): The number of positions to shift each character. 
                If not provided, a random shift between 1 and 26 is used.
    
        Returns:
            str: The encrypted text.

        """
        if not shift: shift = random.randint(1, 26)
        encrypted = []
        for char in text:
            if char.isalpha():
                offset = 65 if char.isupper() else 97
                encrypted.append(chr((ord(char) - offset + shift) % 26 + offset))
            else:
                encrypted.append(char)
        return ''.join(encrypted)

    @staticmethod
    def decrypt(text: str) -> str:
        """
        Args:
            text (str): The encrypted text to be decrypted.
        
        Returns:
            str: The decrypted text, which is the most likely original text.
        """
        max_matches = -1
        best_shift = 0
        for shift in range(1, 26):
            decrypted = CaesarCipher.encrypt(text, -shift)
            matches = sum(word.lower() in ENGLISH_WORDS for word in decrypted.split())
            if matches > max_matches:
                max_matches = matches
                best_shift = shift
        return CaesarCipher.encrypt(text, -best_shift)
    