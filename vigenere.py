def get_text_distribution(text):
    text = text.lower()
    distribution = {}
    total = 0
    for letter in text:
        if ord(letter) < ord('a') or ord(letter) > ord('z'):
            continue
        if letter in distribution:
            distribution[letter] += 1
        else:
            distribution[letter] = 1
        total += 1
    for letter in distribution:
        distribution[letter] = distribution[letter] / total
    return distribution

def chi_squared(d1, d2):
    chi = 0
    for letter in d1:
        if letter in d2:
            chi += ((d1[letter] - d2[letter])**2) / d2[letter]
        else:
            chi += d1[letter]**2
    return chi

def decrypt_text(ciphertext, key):
    ciphertext = ciphertext.lower()
    key_index = 0
    key_length = len(key)
    plaintext = ""
    for letter in ciphertext:
        if letter.isalpha():
            shift = ord(key[key_index]) - ord('a')
            key_index = (key_index + 1) % key_length
            new_pos = ord(letter) - shift
            if new_pos < ord('a'):
                new_pos += 26
            plaintext += chr(new_pos)
        else:
            plaintext += letter
    return plaintext

def vigenere_decrypt(ciphertext, out_file, compare_file="large_english_text.txt"):
    with open(compare_file, 'r') as file:
        compare_text = file.read()
        compare = get_text_distribution(compare_text)

        min_chi = 10
        best_key = ""

        ctext = ''.join([c for c in ciphertext.lower() if c.isalpha()])
        for key_length in range(1, 20):
            sets = ["" for i in range(key_length)]
            for i in range(key_length):
                for j in range(i, len(ctext), key_length):
                    sets[i] = sets[i] + ctext[j]
            key = ""
            for test in sets:
                min_chi_chr = 10
                best_char = ""
                for shift in range(26):
                    check = decrypt_text(test, chr(97 + shift))
                    distribution = get_text_distribution(check)
                    chi = chi_squared(distribution, compare)
                    if chi < min_chi_chr:
                        min_chi_chr = chi
                        best_char = chr(97 + shift)
                key += best_char
            decr = decrypt_text(ciphertext, key)
            distribution = get_text_distribution(decr)
            chi = chi_squared(distribution, compare)
            if chi < min_chi:
                min_chi = chi
                best_key = key
                print(f"Key: {key}  Chi: {chi}")

    out_file.write(f"Key: {best_key}\n\n")
    out_file.write(decrypt_text(ciphertext, best_key))

def decrypt_from_file(file_start):
    file_path = "encrypted4/{}.txt".format(file_start)
    with open(file_path, 'r') as file:
        ciphertext = file.read()
    
    decrypted_file_path = "{}_decrypted.txt".format(file_start)
    with open(decrypted_file_path, 'w') as file:
        vigenere_decrypt(ciphertext, file)

print("Decrypting easy...")
decrypt_from_file("vigerene_easy_encrypted")
print("Decrypting medium...")
decrypt_from_file("vigerne_medium_encrypt")
print("Decrypting hard...")
decrypt_from_file("vigerene_hard_encrypt")
