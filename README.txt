BY: Evan Wheeler
Student# 30046173

FILES:
-encryptFile.py
	Usage: python3 encryptFile.py [plaintext-filename] [tampered-filename] [password]

	Given a plaintext file and a password, the program will encrypt the file as specified
in the question and store the calculated ciphertext in [tamperedFileName] as a binary file.


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

The problem is solved in full with parts a, b, and c being contained in "modifyFile.py"
and part d being done in "encryptFile.py"

There are no known bugs to the program.

If a cyphertext is supplied to modifyFile.py that does not
contain "FOXHOUND" or is encrypted with a password that is not in the form
"YYYYMMDD" from 1984 then the program will print a message stating that this is the case
and then it will exit without writing anything to a file.
