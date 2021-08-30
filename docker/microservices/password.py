import random
import string
from passlib.hash import sha256_crypt

RANDOM_PASSWORD_LENGTH = 30

def generateRandomPassword():
    password = ''.join((random.choice(string.ascii_letters + string.digits) for i in range(RANDOM_PASSWORD_LENGTH)))
    return password

def hashPassword(password):
    hashed = sha256_crypt.hash(password)
    return hashed

