from sys import argv


print('file path: ' + argv[0])
print('amount of args: ' + str (len(argv) -1))
for item in argv[0:]:
    print('arg: ' + item)