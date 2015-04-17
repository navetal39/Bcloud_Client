# Imports: #
from Crypto.Cipher import AES
from Crypto.Hash import SHA256

# Hash func: #
def do_hash(mess):
    hasher = SHA256.new()
    hasher.update(mess)
    return hasher.hexdigest()

# Constants for ecryption: #
BLOCK_SIZE = 32
PADD_CHAR = '?'

# Ecryption funcs: #
def encrypt(plaintext):
    from crypto_extended import generate_key as KEY
    padded_plaintext = padd(plaintext)
    encryptor = AES.new(KEY())
    ciphertext = encryptor.encrypt(padded_plaintext)
    encoded_ciphertext = ciphertext.encode("Base64") # Encoded in base64 for printing and other comforts sake's
    return encoded_ciphertext

def decrypt(encoded_ciphertext):
    from crypto_extended import generate_key as KEY
    decryptor = AES.new(KEY())
    ciphertext = encoded_ciphertext.decode("Base64") #Decode from base64, the reason for encoding is written above.^
    padded_plaintext = decryptor.decrypt(ciphertext)
    return depadd(padded_plaintext)

## Utill for encryption funcs: ##
def padd(not_padded):
    padding_amount = (BLOCK_SIZE - len(not_padded) % BLOCK_SIZE)
    padding = padding_amount * PADD_CHAR
    padded = not_padded + padding
    return padded

def depadd(padded):
    depadded = padded.strip(PADD_CHAR)
    return depadded

''' # For checking:
pt = raw_input('plaintext: ')
print "==========> Encrypted: ", encrypt(pt)

ct = raw_input('ciphertext: ')
print "==========> Decrypted: ", decrypt(ct)
'''

'''
Exciting. Satisfying. Period.
.
'''
