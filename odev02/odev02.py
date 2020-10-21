class Airline:
    def __init__(self,name,partnerList = []):
        self.name = name
        self.partnerList = partnerList
        
    def addNewPartner(self,airline):
        self.partnerList.append(airline)
        
    def hasPartner(self,partner):
        return partner in self.partnerList
        
    def toString(self):
        print(self.name)
        for partner in self.partnerList:
            print(self.name + " -> " + partner.name)
        print("//////----/////-----///")
        
def recursiveSearcher(domain,search,path = []):
#    print(domain.name + " "+ search.name + " ")
    
    if domain not in path:
        path.append(domain)
    else:
        return None
        
    if domain.hasPartner(search):
        path.append(search)
        return path
    else:
        for airline in domain.partnerList:
            p = recursiveSearcher(airline,search,path)
            if p is not None:
                return p
               
                
        
    

import sys

f = open("airlines.txt", "r")
airlines_lines = f.readlines()
airline_dict = {}

for line in airlines_lines:
#    print(line)
    airlineNames = line.split(",")
    name =airlineNames.pop(0).strip()
    airline = Airline(name,[])
    
    try:
        airline = airline_dict[name]
    except:
        airline_dict[name] = airline
        airline = airline_dict[name]
        
    for pAirline in airlineNames:
        pAirline = pAirline.strip()
        try:
            airline.addNewPartner(airline_dict[pAirline])
        except:
            airline_dict[pAirline] = Airline(pAirline,[])
            airline.addNewPartner(airline_dict[pAirline])
    

#for airline in airline_dict.keys():
##    print(airline)
#    airline_dict[airline].toString()

if len(sys.argv) != 3:
    print("Invalid Arguments")
    print("<domain airline name ex: \"Canada Air\">    <searched airline name ex: \"Canada Air\">")
    sys.exit()
try:
    domain = airline_dict[sys.argv[1]]
except:
    print("Invalid domain airline name : " +sys.argv[1])
    print("<domain airline name ex: \"Canada Air\">    <searched airline name ex: \"Canada Air\">")

    sys.exit()
    
try:
    search = airline_dict[sys.argv[2]]
except:
    print("Invalid searched airline name : " + sys.argv[2])
    print("<domain airline name ex: \"Canada Air\">    <searched airline name ex: \"Canada Air\">")

    sys.exit()

res = recursiveSearcher(domain,search,[])
str = "Path ::>> "
if res is not None:
    for airline in res:
        str += " --> "
        str += airline.name
    print(str)
else:
    print("Not found!!")



