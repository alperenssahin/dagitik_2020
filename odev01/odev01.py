import sys
import re

database = {}

if len(sys.argv) < 2 :
    print("Invalid  argument")
    sys.exit()
    
n = int(sys.argv[1])
for i in range(0,n):
    print("Insert User :")
    while True:
        ID = input("ID :")
        try:
            ID = int(ID)
            valid = database[str(ID)]
            print("User ID has already used")
        except ValueError:
            print("ID must be a number")
        except KeyError:
            break
   
    while True:
        name = input("name :")
        if re.search("\d",name):
            print("Name can not include numbers")
        else:
            break
    
    while True:
        surname = input("surname :")
        res = surname.split(" ")
        if len(res) == 1:
            if re.search("\d",surname):
                print("Surname can not include numbers")
            else:
                break
        print("Invalid surname")
    
    while True:
        age = input("age :")
        try:
            age = int(age)
            break
        except ValueError:
            print("Age must be a number")
            
    tupple = (ID,name,surname,age)
    database[str(ID)] = tupple

for key in database.keys():
    print(key + " : ")
    print(database[key])
        
   
