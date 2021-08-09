import sys
import hashlib
def check(args):
	if len(args) != 2:
		print("usage hashme.py <phrase>")
		return False
	return True

def main(phrase):
	salt ='Km5d5ivMy8iexuHcZrsD' 
	hash_obj = hashlib.pbkdf2_hmac('sha512', phrase.encode(), salt.encode(), 200000)
	print(hash_obj.hex())

if check(sys.argv): main(sys.argv[1])
