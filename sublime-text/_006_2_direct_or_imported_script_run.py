import _005_1_direct_or_imported_script_run

print("Top level in two.py")

_005_1_direct_or_imported_script_run.func()

if __name__ == '__main__':
	print("two.py is being run directly")
else:
	print("two.py has been imported")