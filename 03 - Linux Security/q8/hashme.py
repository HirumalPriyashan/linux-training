import sys
import uuid
import hashlib
def check(args):
	if len(args) != 2:
		print("usage hashme.py <phrase>")
		return False
	return True

def main(phrase):
	salt = uuid.uuid4().hex # generate random salt
	# print('salt: ' + salt)
	hash_obj = hashlib.sha512(phrase.encode + salt.encode()).hexdigest()
	print(hash_obj)

if check(sys.argv): main(sys.argv[1])
