#!/usr/bin/env python3

from Crypto.Cipher import AES
import os, codecs

def pad(msg):
	val = 16 - (len(msg) % 16)
	pad_data = msg + (chr(val) * val)
	return pad_data

def encrypt(key, iv, msg):
	cipher = AES.new(key, AES.MODE_CBC, iv)
	enc = cipher.encrypt(msg)
	print(codecs.encode(enc, 'hex'))

def get_input_then_encrypt():
	key = KEY
	iv = IV
	msg = input("Input the message you want to encrypt: ")
	msg = codecs.encode(pad(msg))
	choice = input("Would you like to input a custom key? (y/n): ")
	if(choice == 'y' or choice == 'Y'):
		key = input("Input custom key: ")
	choice = input("Would you like to input a custom IV? (y/n): ")
	if(choice == 'y' or choice == 'Y'):
		iv = input("Input custom IV: ")
	encrypt(msg, iv, key)

def menu():
	print("1) Encrypt a message")
	print("2) Encrypt the flag")
	print("3) Exit")

def main():
	try:
		while True:
			menu()
			choice = int(input("Choice: "))
			if choice == 1:
				get_input_then_encrypt()
			elif choice == 2:
				aes = AES.new(KEY, AES.MODE_CBC, IV)
				print(codecs.encode(aes.encrypt(FLAG), 'hex'))
			else:
				print("Bye bye~")
				exit()
	except Exception as e:
		print("You broke something...")
		exit()

if __name__=='__main__':
	KEY = os.urandom(16)
	IV = os.urandom(16)
	FLAG = pad(open('flag.txt', 'r').read())
	main()