import argparse
import hashlib
import json

charactersets={
    "l":"abcdefghijklmnopqrstuvwxyz",
    "U":"ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "0":"0123456789",
    "!":"!\"#$%&\'*+,-./:;=?@~^_|",
    "(":["()","[]","{}","<>"]
}

letterSwapMap={'a': '4', 'b': '8', 'c': '(', 'd': '[', 'e': '6', 'f': '=', 'g': '9', 'h': '}{', 'i': '|', 'j': '/', 'k': 'X', 'l': '_', 'm': 'w', 'n': 'M', 'o': '0', 'p': '?', 'q': ',', 'r': '&', 's': '$', 't': '7', 'u': '|_|', 'v': '\/', 'w': '#', 'x': '%', 'y': ';', 'z': '2'}

wordset=[]
with open("wordset_20K.json","r") as f:
    wordset=json.load(f)

parse = parser = argparse.ArgumentParser(
                    prog='Password Generator',
                    description='',
                    epilog='')
parser.add_argument("-s","--servicename",
    help="Enter the name of the Service you are planning to use the password for, be consistent with the format. eg. Paypal")
parser.add_argument("-m","--masterpassword",required=False,
    help="Enter your master password here. Make sure to remember it.")
parser.add_argument("-mh","--masterpasswordHash",required=False,
    help="Enter your master password hash, passwordgen uses sha3_512")
parser.add_argument("-pv","--preversionHash",required=False,
    help="Enter your hash(hash(masterpassword)+service) manualty")
parser.add_argument("-v","--version",default="001",
    help="Enter version of your password")
parser.add_argument("-cs","--charactersets",default="lU0!",
    help="Enter version of your password")
arguments = parser.parse_args()

class HashFeeder:
    def __init__(self,hash):
        self.hash=hash
        self.hexCharI=-1
        self.bitIndex=4
        self.bits=[]
    def feed(self):
        if self.bitIndex>2:
            self.hexCharI+=1
            if self.hexCharI>=len(self.hash):
                return None
            self.bits=list(map(int,bin(int(self.hash[self.hexCharI],16))[2:].zfill(4)))
            self.bitIndex=-1
        self.bitIndex+=1
        return self.bits[self.bitIndex]

#binary search
def selectRandom(hashFeeder,startI,endI):
    length=endI-startI+1
    if length==1:
        return startI
    odd=0 # odd is actually opposite. If True do not include 
    if length%2:
        odd=hashFeeder.feed()
    
    if hashFeeder.feed():
        return selectRandom(hashFeeder, (startI+endI+1)//2-odd, endI)
    else:
        return selectRandom(hashFeeder, startI, (startI+endI-1)//2+odd)

if __name__ == "__main__":
    masterpasswordHash=arguments.masterpasswordHash
    if masterpasswordHash==None:
        masterpasswordHash=hashlib.sha3_256(arguments.masterpassword.encode()).digest().hex()
    hashFeeder=HashFeeder(masterpasswordHash)
    password=""
    #requerment meeter
    brakets=charactersets["("][selectRandom(hashFeeder, 0, len(charactersets["("])-1)]
    password+=brakets[0]
    password+=charactersets["l"][selectRandom(hashFeeder, 0, len(charactersets["l"])-1)]
    password+=charactersets["U"][selectRandom(hashFeeder, 0, len(charactersets["U"])-1)]
    password+=charactersets["0"][selectRandom(hashFeeder, 0, len(charactersets["0"])-1)]
    password+=charactersets["!"][selectRandom(hashFeeder, 0, len(charactersets["!"])-1)]
    password+=brakets[1]
    #word
    brakets=charactersets["("][selectRandom(hashFeeder, 0, len(charactersets["("])-1)]
    password+=brakets[0]
    word=list(wordset[selectRandom(hashFeeder, 0, len(wordset))])
    for i in range(len(word)):
        if hashFeeder.feed():
            if hashFeeder.feed():
                word[i]=word[i].upper()
            else:
                word[i]=letterSwapMap[word[i]]
    password+="".join(word)
    password+=brakets[1]
    #numebr
    brakets=charactersets["("][selectRandom(hashFeeder, 0, len(charactersets["("])-1)]
    password+=brakets[0]
    password+=str(selectRandom(hashFeeder, 0, 999999))
    password+=brakets[1]
    print(password)
    
    


        




