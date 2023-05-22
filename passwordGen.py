import argparse
import hashlib
import json
import pyperclip
import getpass
import time
import yaml #Put all of the preferences into yaml

with open("config.yaml","r") as f:
    config=yaml.safe_load(f)

characters=config["characters"]
letterSwapMap=config["letterSwapMap"]
hexString=config["endnumbers"]

#all words are at least 8-22 long and lowercase
wordset=[]
with open("elementWordList.json","r") as f:
    wordset=json.load(f)

parse = parser = argparse.ArgumentParser(
                    prog='Password Generator',
                    description='',
                    epilog='')
parser.add_argument("-s","--service", default=config["default-service"],
    help="Enter the name of the Service you are planning to use the password for, be consistent with the format. eg. Paypal")
parser.add_argument("-e","--extra",required=False,
    help="Enter secondary pass phrase/password could be the login")
parser.add_argument("-v","--version",default="001",
    help="Enter version of your password")
parser.add_argument("-cs","--characterset",default=config["characterset"],
    help="Enter version of your password")
parser.add_argument("-ht","--hashtype",default="sha3_256",
    help="Enter version of your password")
parser.add_argument("--copy",action="store_const",const=True,default=False,help="Copies password to clipboard")
parser.add_argument("-d","--display",action="store_const",const=True,default=False,help="Displays the password in the terminal")
arguments = parser.parse_args()

#TODO implement charactersets

class HashFeeder:
    def __init__(self,hash):
        self.hash=hash
        self.hexCharI=-1
        self.bitIndex=4
        self.bits=[]
        self.strength=0
    def feed(self):
        if self.bitIndex>2:
            self.hexCharI+=1
            if self.hexCharI>=len(self.hash):
                return None
            self.bits=list(map(int,bin(int(self.hash[self.hexCharI],16))[2:].zfill(4)))
            self.bitIndex=-1
        self.bitIndex+=1
        self.strength+=1
        return self.bits[self.bitIndex]
    def getStrength(self):
        return self.strength

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

def generateBracets(hashFeeder,charactersets):
    return config["parethesis"][selectRandom(hashFeeder, 0, len(config["parethesis"])-1)] #FIXME this part still uses config

def generateWord(hashFeeder,wordset):
    word=""
    while len(word)<18:
        addition=list(wordset[selectRandom(hashFeeder, 0, len(wordset)-1)])
        #swap some letters
        for i in range(len(addition)):
            if hashFeeder.feed():
                addition[i]=letterSwapMap[addition[i].lower()]
            elif len(addition)>2:
                if hashFeeder.feed():
                    addition[i]=addition[i].upper()
        word+="".join(addition)
        
    return word[:18]

def generatePassword(hashFeeder,wordset,charactersets):
    password=""
    #requerment meeter
    brakets=generateBracets(hashFeeder, charactersets)
    password+=brakets[0]
    for character in charactersets:
        password+=characters[character][selectRandom(hashFeeder, 0, len(characters[character])-1)]
    password+=brakets[1]
    #words
    brakets=generateBracets(hashFeeder, charactersets)
    password+=brakets[0]
    password+=generateWord(hashFeeder, wordset)
    password+=brakets[1]
    #number
    brakets=generateBracets(hashFeeder, charactersets)
    password+=brakets[0]
    for i in range(25,31):
        password+=hexString[selectRandom(hashFeeder, 0, 15)]
    password+=brakets[1]

    print("Password Strength:",hashFeeder.getStrength())
    return password

def hashfunction(bytestring,hashtype,hashlib):
    if hashtype=="sha3_256":
        return hashlib.sha3_256(bytestring).digest()
    if hashtype=="md5":
        return hashlib.md5(bytestring).digest()
    

if __name__ == "__main__":
    #parsing
    hashtype=arguments.hashtype
    masterpassword=getpass.getpass("Masterpassword:").encode()
    service=arguments.service.encode()
    version=b"v"+int(arguments.version).to_bytes(1, byteorder="big")
    extra=arguments.extra

    characterset=arguments.characterset
    display=arguments.display
    copy=arguments.copy
    
    #hashing
    masterpasswordHash=hashfunction(masterpassword, hashtype, hashlib)
    masterAndServiceHash=hashfunction(masterpasswordHash+service, hashtype, hashlib)
    extraHash=b""
    if extra!=None:
        extraHash=hashfunction(extra.encode(), hashtype, hashlib)
    finalHash=hashfunction(masterAndServiceHash+extraHash+version, hashtype, hashlib).hex()
    hashFeeder=HashFeeder(finalHash)
    #Generate
    password=generatePassword(hashFeeder,wordset,characterset)

    #Display
    if display:
        print(password)
    if copy:
        pyperclip.copy(password)
        time.sleep(config["clipboard-timeout"]) #TODO add this into the yaml settings
        pyperclip.copy(" ")
        
    
    


        




