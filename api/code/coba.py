import os

if not os.path.exists('asd/Try.c'):
	os.mkdir("asd/test")
	os.open('asd/Try.c', os.O_CREAT)