A pair of python programs that use the python cryptography module to first encrypt a file, then brute-forces a password to read the file and (possibly) modifies the plain-text message before writing it to a file.

FILES:
-encryptFile.py
	Usage: python3 encryptFile.py [plaintext-filename] [tampered-filename] [password]

	Given a plaintext file and a password, the program will encrypt the file as specified below and store the calculated ciphertext in [tamperedFileName] as a binary file.
	-Converts the plaintext to byte array 'B'
	-Computes a hash tag  't' on the plaintext by using SHA1 (I know it is depreciated, ann would not use it in a real-life implementation.
	-Derives and encryption key by using SHA1 on the password and truncating for AES-128 (also could be 256 in a real implementation)
	-Generates a 16-byte IV (for CBC mode)
	-Padds  (B || t) using PKCS7 if necessary, and then encrypts the array with AES128 in CBC mode.
	-The program then writes the IV, followed by the encryption to the specified file name.
	


-modifyFile
	Usage: python3 modifyFile [ciphertext-filename]

	Given the cyphertext, the program will brute force the password by iterating through
all dates from "19840101" to "20201231" and decrypting the file using the date string as
the key. The program does this by looking for the string "FOXHOUND" in the decrypted plaintext.
Once the program finds the key, it prints it out to the terminal.
Then the program will replace the string "CODE-RED" with "CODE-BLUE" if it exists in the plaintext.
Finally the program writes the (possibly modified) plaintext to a file.

***The name of the file that the program writes the plaintext to is specified on line #20
By default it will write to "palintext.txt" however this can be changed by modifying the string
on line #20***

If a cyphertext is supplied to modifyFile.py that does not
contain "FOXHOUND" or is encrypted with a password that is not in the form
"YYYYMMDD" from 1984 then the program will print a message stating that this is the case
and then it will exit without writing anything to a file.
