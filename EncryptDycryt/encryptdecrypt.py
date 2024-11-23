from cryptography.fernet import Fernet

#generate the key
key = Fernet.generate_key()
#string the key into a file
with open('unlock.key', 'wb') as unlock:
     unlock.write(key)
     
#open the key
with open('unlock.key', 'rb') as unlock:
     key = unlock.read()
print(key)     


#use the generated key
f = Fernet(key)
#open the original file to encrypt
with open('const.py', 'rb') as original_file:
     original = original_file.read()
#encrypt the file
encrypted = f.encrypt(original)
#you can write the encrypted data  file into a enc_sample.txt
with open ('enc_const.py', 'wb') as encrypted_file:
     encrypted_file.write(encrypted)
     
     
#first use the key
f = Fernet(key)
#open the encrypted file
with open('enc_const.py', 'rb') as encrypted_file:
     encrypted = encrypted_file.read()
#decrypt the file
decrypted = f.decrypt(encrypted)
#finally you can write the decrypted file into a dec_sample.txt
with open('dec_const.py', 'wb') as decrypted_file:
     decrypted_file.write(decrypted)     