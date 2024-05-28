def caesar_decrypt(ciphertext, shift):
    decrypted_text = ''
    for char in ciphertext:
        if char.isalpha():
            new_pos = ord(char) - shift
            if char.islower():
                if new_pos < ord('a'):
                    new_pos += 26
            elif char.isupper():
                if new_pos < ord('A'):
                    new_pos += 26
            decrypted_text += chr(new_pos)
        else:
            decrypted_text += char
    return decrypted_text

def decrypt_from_file(file_path):
    with open(file_path, 'r') as file:
        ciphertext = file.read()
    
    decrypted_file_path = "caesar_easy_2_decrypted.txt"
    with open(decrypted_file_path, 'w') as decrypted_file:
        for shift in range(26):
            decrypted_text = caesar_decrypt(ciphertext, shift)
            decrypted_file.write("Shift: {}\n".format(shift))
            decrypted_file.write("Decrypted Text:\n{}\n".format(decrypted_text))

file_path = "encrypted4/caesar_easy_2_encrypted.txt"
decrypt_from_file(file_path)
