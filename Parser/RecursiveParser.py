import sys
sys.path.append("..")

import json
from Tokenizer.Token import Token

Token_List = []
i = 0
TreeNodes={"Program":[]}

def RecurParse(path):
    global i,Token_List
    f = open(path,"r")
    Token_List = [Token.unserilze(i.strip()) for i in f.readlines()]
    print(len(Token_List))
    Program()
    print("Done")
    
    

def Program():
    ProgramHead()
    DeclarePart()
    ProgramBody()
    match("END_PROGRAM")


def ProgramHead():
    match("PROGRAM")
    ProgramName()

def ProgramName():
    match("ID")

def  DeclarePart():
    TypeDecpart()
    VarDecpart()
    ProcDecpart()


def    TypeDecpart():
    pass
def    VarDecpart():
    pass
def    ProcDecpart():
    pass

def ProgramBody():
    pass

def match(strings:str):
    global i,Token_List

    if Token_List[i].type == strings:
        print(strings)
        i+=1
        return
    else:
        raise TypeError(strings)
    


if __name__ == "__main__":
    rules = json.load(open("rules.json"))
    RecurParse("temp.tok")