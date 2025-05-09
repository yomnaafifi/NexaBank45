import random
# import English words

class CaesarCipher:
    @staticmethod
    def encrypt(text: str, shift=None):
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
    def decrypt(text):
        max_matches = -1
        best_shift = 0
        for shift in range(1, 26):
            decrypted = CaesarCipher.encrypt(text, -shift)
            matches = sum(word.lower() in valid_words for word in decrypted.split())
            if matches > max_matches:
                max_matches = matches
                best_shift = shift
        return CaesarCipher.encrypt(text, -best_shift)
    