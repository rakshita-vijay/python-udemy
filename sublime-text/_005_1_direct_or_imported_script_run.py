def func():
	print("In one.py")

print("Top level of one.py")

if __name__ == '__main__':
	print("one.py is being run directly")
else:
	print("one.py has been imported")