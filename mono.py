import random
import math
import nltk

def get_all_words(text):
    words = []
    word = ""
    for letter in text.lower():
        if letter.isalpha():
            word += letter
        else:
            if word != "":
                words.append(word)
                word = ""
    if word != "":
        words.append(word)
    return words

def get_word_dist(text):
    total = 0
    distribution = {}
    for word in get_all_words(text):
        if word in distribution:
            distribution[word] += 1
        else:
            distribution[word] = 1
        total += 1
    for item in distribution:
        distribution[item] = distribution[item] / total
    return distribution

def get_letter_dist(text):
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

def reverse_key(key):
    reverse = ['a' for i in range(26)]
    for i in range(26):
        reverse[ord(key[i]) - ord('a')] = chr(i + ord('a'))
    return ''.join(reverse)

def decrypt_text(ciphertext, key):
    ciphertext = ciphertext.lower()
    plaintext = ""
    for letter in ciphertext:
        if letter.isalpha():
            plaintext += key[ord(letter) - ord('a')]
        else:
            plaintext += letter
    return plaintext

def key_swap(key):
    key = list(key)
    i, j = random.randint(0, 25), random.randint(0, 25)
    key[i], key[j] = key[j], key[i]
    return ''.join(key)

def mono_decrypt(ciphertext, out_file, compare_file="large_english_text.txt"):
    with open(compare_file, 'r') as file:
        compare_text = file.read()
        for word in nltk.corpus.words.words():
            compare_text += word + " "
        compare_dist = get_word_dist(compare_text)
        compare_letter_dist = get_letter_dist(compare_text)
        def log_prob(text):
            prob = 0
            dist = get_word_dist(text)
            letter = get_letter_dist(text)
            for c in letter:
                prob += math.log(compare_letter_dist[c])
            for c in dist:
                if c in compare_dist:
                    prob += math.log(compare_dist[c])
                else:
                    prob += math.log(1 / (len(compare_dist) * 2))

            return prob

        key = "abcdefghijklmnopqrstuvwxyz"
        best_score = log_prob(decrypt_text(ciphertext, key))
        last_score = best_score
        last_key = key
        for i in range(100000):
            new_key = key_swap(last_key)
            new_score = log_prob(decrypt_text(ciphertext, new_key))
            prob = math.exp(new_score - last_score)
            if random.random() < prob:
                last_score = new_score
                last_key = new_key
            if new_score > best_score:
                best_score = new_score
                key = new_key
        plaintext = decrypt_text(ciphertext, key)
        out_file.write(f"Key: {reverse_key(key)}\n\n")
        out_file.write(plaintext)

def decrypt_from_file(file_start):
    file_path = "encrypted4/{}.txt".format(file_start)
    with open(file_path, 'r') as file:
        ciphertext = file.read()
    
    decrypted_file_path = "{}_decrypted.txt".format(file_start)
    with open(decrypted_file_path, 'w') as file:
        mono_decrypt(ciphertext, file)

print("Decrypting easy...")
decrypt_from_file("mono_easy_encrypt")
print("Decrypting medium...")
decrypt_from_file("mono_medium_encrypt")
