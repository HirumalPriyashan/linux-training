import sys
import uuid
import hashlib
def check(args):
	if len(args) != 2:
		print("usage hashme.py <phrase>")
		return False
	return True

def main(phrase):
	salt = uuid.uuid4().hex
	print('salt: ' + salt)
	hash_obj = hashlib.pbkdf2_hmac('sha512', phrase.encode(), salt.encode(), 200000)
	print(hash_obj.hex())

if check(sys.argv): main(sys.argv[1])
