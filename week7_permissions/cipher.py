from cryptography.fernet import Fernet


# key = Fernet.generate_key()
key = b'sghpe4geeouafegea468age4a8e64gea6gaege53ea8='
# Fp0prYWHfoPjMdBtE0Wxt217aDIyeN3UAR5519vspTs=
# sghpe4geeouafegea468age4a8e64gea6gaege53ea8=
f = Fernet(key)
print(key)

plaintext = b"Lets encrypt this \o/"

ciphertext = f.encrypt(plaintext)
print(ciphertext)

decryptedtext = f.decrypt(ciphertext)
print(decryptedtext)