from sys import path as syspaths
print("\n----------------")
print("Första 10")
print("\n")
for item in syspaths[0:10]:
    print(item)
print("\n\n"
"----------------")
print("Sista 10\n")
for item in syspaths[-10:]:
    print(item)