from cryptography.fernet import Fernet
import random
import hashlib
 



fernet = Fernet(b'il4gsK-SJ4PUeygJseQ7W7KJ7mbIFU6cePBa3DeAWYM=')
decMessage = fernet.decrypt(b'gAAAAABisrwT1wpAAhlM7MV3K-47SKvFyQZI92Bgp9By1pC572zk_aD-MI9R491h5OLee1cysVsrxE-bBIgA88K2UTiJWIIIxg==').decode()
print("decrypted string: ", decMessage)


def randOtp(length):
    sample_string = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'  # define the specific string
    return ''.join((random.choice(sample_string)) for x in range(length))


otp = randOtp(8)
otphash = hashlib.md5(otp.encode())

print(otphash.hexdigest())