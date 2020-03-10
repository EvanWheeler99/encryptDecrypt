"""
encryptFile.py
Usage: python3 encryptFile.py [plaintext-filename] [tampered-filename] [password]

Name: Evan Wheeler
Student# 30046173
"""


# Imports
import sys
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import padding


# inputs:	b (the plaintext casted to bytes)
# 			password (the password to use as a key for the encryption)
#
# returns:	bites, the iv concatonated with the encryted ciphertext
def encryptFoxhound(b, password):

	# Computes a hash tag t on the plaintext by applying SHA1 to the byte array B
	digest = hashes.Hash(hashes.SHA1(), backend = default_backend())
	digest.update(b)
	hashtag = digest.finalize()

	# appends t to B to obtain an extended byte array
	bPrime = b + hashtag

	# Create the SHA1 hash for the password
	digest = hashes.Hash(hashes.SHA1(), backend = default_backend())
	digest.update(password.encode())
	hashedPass = digest.finalize()

	# Truncate password
	truncatedPass = hashedPass[:-4]		#20 - 16 = 4 bytes to truncate

	# Generates a random 16-byte initial value IV (for use in CBC mode)
	iv = os.urandom(16)

	# Pads the extended byte array B' using the PKCS7 format if necessary
	padder = padding.PKCS7(128).padder()
	bPrimePadded = padder.update(bPrime) + padder.finalize()

	# encrypts the padded array with AES-128-CBC
	cipher = Cipher(algorithms.AES(truncatedPass), modes.CBC(iv), backend= default_backend())
	# Encrypt the ciphertext
	encryptor = cipher.encryptor()
	return iv + encryptor.update(bPrimePadded) + encryptor.finalize()


if __name__ == '__main__':
	if (len(sys.argv) != 4):
		print("Usage: python3 encryptFile.py [plaintext-filename] [tampered-filename] [password]")
		exit()

	plaintextFileName = sys.argv[1]
	tamperedFileName = sys.argv[2]
	password = sys.argv[3]

	b = open(plaintextFileName, "rb").read()	#Read bytes

	#get the iv + encrypted ciphertext
	message = encryptFoxhound(b, password)

	# appends the iv concatonated with the resulting ciphertext to the file F.
	f = open(tamperedFileName, "wb")			#Write bytes
	f.write(message)
	f.close()
