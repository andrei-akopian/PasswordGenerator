import yaml
"""
Script responsible for generating a random word
"""

with open("wordGenerator/wordparts.yaml","r") as f:
    wordparts=yaml.safe_load(f)

def generateWord(hashFeeder,selectRandom,length):
    word=""
    current_letter_type=hashFeeder.feed() #0 for vowels, 1 for constants
    i=0
    while i<length:
        if current_letter_type:
            #new constant
            current_letter_type=hashFeeder.feed()
            if current_letter_type:
                #double
                if hashFeeder.feed() and len(word)>1:
                    word+=word[len(word)-1]
                #new
                else:
                    word+=wordparts["constants"][selectRandom(hashFeeder,0,len(wordparts["constants"])-1)]
            #new vowel after constant
            else:
                word+=wordparts["vowels"][selectRandom(hashFeeder,0,len(wordparts["vowels"])-1)]
        #vowel -> has to be a constant
        else:
            word+=wordparts["constants"][selectRandom(hashFeeder,0,len(wordparts["constants"])-1)]
            current_letter_type=1
        i+=1
    return word
