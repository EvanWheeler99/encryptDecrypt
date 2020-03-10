"""
encryptFile.py
Usage: python3 modifyFile [ciphertext-filename]

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


# The name of the output file
PLAINTEXTFILE = "plainText.txt"		#change this line to change what file the program writes to


# inputs:	pswd (the key to the ciphertext)
# 			IV (the iv of the file),
# 			cipherText (the emaining ciphertext in the file)
#
# returns:	string, the plaintext decryption of the ciphertext
def decodeWithPass(cipherText, iv, pswd):

	# Create the SHA1 hash for the password
	digest = hashes.Hash(hashes.SHA1(), backend = default_backend())
	digest.update(pswd.encode())
	hashedPass = digest.finalize()

	# Truncate password
	truncatedPass = hashedPass[:-4]		#20 - 16 = 4 bytes to truncate

	# Create cipher object
	cipher = Cipher(algorithms.AES(truncatedPass), modes.CBC(iv), backend= default_backend())

	# Decrypt the ciphertext
	decryptor = cipher.decryptor()
	message = decryptor.update(cipherText) + decryptor.finalize()

	# Strip the padding
	unpadder = padding.PKCS7(128).unpadder()
	plaintext = unpadder.update(message) + unpadder.finalize()

	# Remove the hashtag (We know the SHA1 hash is 20 bytes so we can strip of the last 20 bytes of the array)
	plaintext = plaintext[:-20]

	# cast from bytes to string and returns the plaintext
	return plaintext.decode("utf-8")


# inputs:	substring (the string to search for in the text)
# 			thiCCText (the plaintext search space)
#
# returns:	boolean, if the substring in the text
def isSubstring(substring, thiCCText):
	if substring in thiCCText:
		return True
	return False


# inputs:	cipherText (the byte array representing the cyphertext)
# 			IV (the iv of the cyphertext found in the file)
#
# returns:	string, the bruteforced password   (will be None if the password cannot be brute forced)
# 			string, the contents fof the plaintext file
def bruteForcePassword(cipherText, IV):
	year = 1984
	while (year < 2021):
		for month in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
			for day in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12",  "13", "14", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31"]:
				password = str(year) + month + day

				try:
					potentialPT = decodeWithPass(cipherText, IV, password)
					if (isSubstring("FOXHOUND", potentialPT)):
						return ( password, potentialPT)
				except:
					continue
		year += 1
	return (None, None)	#Only gets here if the password cannot be brute forced


if __name__ == '__main__':
	if (len(sys.argv) != 2):
		print("Usage: python3 modifyFile.py [ciphertext-filename]")
		exit()
	ciphertextFileName = sys.argv[1]

	# Open the ciphertext file and store the iv / ciphertext
	inputFile = open(ciphertextFileName, "rb")
	iv = inputFile.read(16)							#The IV is stored in the first 16 bytes of the file
	ct = inputFile.read()							#The rest of the file is the cyphertext
	inputFile.close()								#Close the file


	# Brute force the password and return it
	(password, plaintext) = bruteForcePassword(ct, iv)

	if (password is None):
		print("The password is not within the specified range OR FOXHOUND is not in the plaintext")
		sys.exit()

	# Print the password to terminal
	print("Password: " + password)

	# Replace "CODE-RED" with "CODE-BLUE" if it exists
	plaintext = plaintext.replace("CODE-RED", "CODE-BLUE")

	# Write the plaintext to PLAINTEXTFILE
	outputFile = open(PLAINTEXTFILE, "w")
	outputFile.write(plaintext)
	outputFile.close()
