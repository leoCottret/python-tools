from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import getpass
import argparse

# Usage:
# Generate key          -> python3 sfe.py -g -k "secret.key"
# Encrypt file with key -> python3 sfe.py -e -k "secret.key" -i "file_to_encrypt.txt" -o "encrypted_file.afe_enc"
# Decrypt file with key -> python3 sfe.py -d -k "secret.key" -i "encrypted_file.afe_enc" -o "decrypted_file.txt"

parser = argparse.ArgumentParser(description='A tool to encrypt/decrypt a file with AES-256 encryption')
parser.add_argument('-g', '--generate-key', action='store_true', help='generate AES-256 key in secret.key file') 
parser.add_argument('-k', '--key-file-name', help='the name of the file that will contain the AES-256 key', required=True) 
parser.add_argument('-e', '--encrypt', action='store_true', help='encrypt file mode') 
parser.add_argument('-d', '--decrypt', action='store_true', help='decrypt file mode') 
parser.add_argument('-i', '--input', help='the "in" file path, the file to encrypt in encrypt mode, and the one to decrypt in decrypt mode') 
parser.add_argument('-o', '--output', help='the "out" file path, the encrypted file in encrypt mode, and the decrypted file in decrypt mode') 
args = parser.parse_args()

NOONCE_MESSAGE = "Enter your secret noonce (you will need both the key file and the noonce to decrypt the file):"

# -----GENERATE NEW KEY-----

# Create key file
# 32 bytes for 32x8=256 bits long -> key for AES-256 encryption
def generate_key_file(keyFile):
	key = get_random_bytes(32).hex()
	key_file = open(keyFile, "w")
	key_file.write(key)
	key_file.close()


# -----ENCRYPT-----
def encrypt_file(fileIn, fileOut, keyFile):
	# get key value
	key = ""
	with open(keyFile, "r") as f:
		key = bytearray.fromhex(f.read())
	# Create file to encrypt data as binary
	file_in=""
	with open(fileIn, "rb") as f:
	    file_in = f.read()

	nonce_str = getpass.getpass(prompt=NOONCE_MESSAGE)

	# Create encrypted file
	cipher = AES.new(key, AES.MODE_EAX, nonce=bytes(nonce_str, "utf-8"))
	ciphertext, tag = cipher.encrypt_and_digest(file_in)
	file_out = open(fileOut, "wb")
	file_out.write(base64.b64encode(ciphertext))
	file_out.close()


# -----DECRYPT-----
def decrypt_file(fileIn, fileOut, keyFile):
	# Get key from file
	key=""
	with open(keyFile, "r") as f:
		key = bytearray.fromhex(f.read())
	nonce_str = getpass.getpass(prompt=NOONCE_MESSAGE)
	cipher = AES.new(key, AES.MODE_EAX, nonce=bytes(nonce_str, "utf-8"))

	# Get encrypted file data
	file_in=""
	with open(fileIn, "r") as f:
		file_in = base64.b64decode(f.read())

	# Create decrypted file with key
	file_out = open(fileOut, "wb")
	file_out.write(cipher.decrypt(file_in))
	file_out.close()

# -----SHARED-----
def print_help_msg(msg):
	print(f'\n{msg}\n\n')
	parser.print_help()
	print("Examples:")
	print('Generate key -> python3 sfe.py -g -k "secret.key"')
	print('Encrypt file with key -> python3 sfe.py -e -k "secret.key" -i "file_to_encrypt.txt" -o "encrypted_file.afe_enc"')
	print('Decrypt file with key -> python3 sfe.py -d -k "secret.key" -i "encrypted_file.afe_enc" -o "decrypted_file.txt"')
	exit()

# -----MAIN-----



if (args.generate_key):
	generate_key_file(args.key_file_name)
if (args.encrypt or args.decrypt):
	if (not args.input or not args.output):
		print_help_msg("You need both an input and output path file")
	if (args.encrypt and args.decrypt):
		print_help_msg("You probably don't want to encrypt and decrypt a file at the same time")
	if (args.generate_key and args.decrypt):
		print_help_msg("You can't create a new key file and try to decrypt a file at the same time, that would make no sense")
	if (args.encrypt):
		encrypt_file(args.input, args.output, args.key_file_name)
	if (args.decrypt):
		decrypt_file(args.input, args.output, args.key_file_name)

if (not (args.encrypt or args.decrypt or args.generate_key)):
	print_help_msg("This did nothing, please look at the examples")