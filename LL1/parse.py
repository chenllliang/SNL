from queue import Queue
from LL1.LL1Parser import * 
# from LL1Parser import Node,Parser_Tree
import json
import sys
sys.path.append("..")
from Tokenizer.Token import Token
import json
from queue import Queue
G = [
            ["Program","ProgramHead","DeclarePart","ProgramBody","END_PROGRAM"],
            ["ProgramHead","PROGRAM","ProgramName"],
            ["ProgramName","ID"],
            ["DeclarePart","TypeDecpart","VarDecpart","ProcDecpart"],
            ["TypeDecpart",""],
            ["TypeDecpart","TypeDec"],
            ["TypeDec","TYPE","TypeDecList"],
            ["TypeDecList","TypeId","EQUAL","TypeDef","SEMICOLON","TypeDecMore"],
            ["TypeDecMore",""],
            ["TypeDecMore","TypeDecList"],
            ["TypeId","ID"],
            ["TypeDef","BaseType"],
            ["TypeDef","StructureType"],
            ["TypeDef","ID"],
            ["BaseType","INTEGER"],
            ["BaseType","CHAR"],
            ["StructureType","ArrayType"],
            ["StructureType","RecType"],
            ["ArrayType","ARRAY","LB","NUMBER","RANGE","NUMBER","RB","OF","BaseType"],
            ["Low","NUMBER"],
            ["Top","NUMBER"],
            ["RecType","RECORD","FieldDecList","END"],
            ["FieldDecList","BaseType","IdList","SEMICOLON","FieldDecMore"],
            ["FieldDecList","ArrayType","IdList","SEMICOLON","FieldDecMore"],
            ["FieldDecMore",""],
            ["FieldDecMore","FieldDecList"],
            ["IdList","ID","IdMore"],
            ["IdMore",""],
            ["IdMore","COMMA","IdList"],
            ["VarDecpart",""],
            ["VarDecpart","VarDec"],
            ["VarDec","VAR","VarDecList"],
            ["VarDecList","TypeDef","VarIdList","SEMICOLON","VarDecMore"],
            ["VarDecMore",""],
            ["VarDecMore","VarDecList"],
            ["VarIdList","ID","VarIdMore"],
            ["VarIdMore",""],
            ["VarIdMore","COMMA","VarIdList"],
            ["ProcDecpart",""],
            ["ProcDecpart","ProcDec"],
            ["ProcDec","PROCEDURE","ProcName","LP","ParamList","RP","SEMICOLON","ProcDecPart","ProcBody","ProcDecMore"],
            ["ProcDecMore",""],
            ["ProcDecMore","ProcDec"],
            ["ProcName","ID"],
            ["ParamList",""],
            ["ParamList","ParamDecList"],
            ["ParamDecList","Param","ParamMore"],
            ["ParamMore",""],
            ["ParamMore","SEMICOLON","ParamDecList"],
            ["Param","TypeDef","FormList"],
            ["Param","VAR","TypeDef","FormList"],
            ["FormList","ID","FidMore"],
            ["FidMore",""],
            ["FidMore","COMMA","FormList"],
            ["ProcDecPart","DeclarePart"],
            ["ProcBody","ProgramBody"],
            ["ProgramBody","BEGIN","StmList","END"],
            ["StmList","Stm","StmMore"],
            ["StmMore",""],
            ["StmMore","SEMICOLON","StmList"],
            ["Stm","ConditionalStm"],
            ["Stm","LoopStm"],
            ["Stm","InputStm"],
            ["Stm","OutputStm"],
            ["Stm","ReturnStm"],
            ["Stm","ID","AssCall"],
            ["AssCall","AssignmentRest"],
            ["AssCall","CallStmRest"],
            ["AssignmentRest","VariMore","ASSIGN","Exp"],
            ["ConditionalStm","IF","RelExp","THEN","StmList","ELSE","StmList","FI"],
            ["LoopStm","WHILE","RelExp","DO","StmList","ENDWH"],
            ["InputStm","READ","LP","Invar","RP"],
            ["Invar","ID"],
            ["OutputStm","WRITE","LP","Exp","RP"],
            ["ReturnStm","RETURN"],
            ["CallStmRest","LP","ActParamList","RP"],
            ["ActParamList",""],
            ["ActParamList","Exp","ActParamMore"],
            ["ActParamMore",""],
            ["ActParamMore","COMMA","ActParamList"],
            ["RelExp","Exp","OtherRelE"],
            ["OtherRelE","CmpOp","Exp"],
            ["Exp","Term","OtherTerm"],
            ["OtherTerm",""],
            ["OtherTerm","AddOp","Exp"],
            ["Term","Factor","OtherFactor"],
            ["OtherFactor",""],
            ["OtherFactor","MultOp","Term"],
            ["Factor","LP","Exp","RP"],
            ["Factor","NUMBER"],
            ["Factor","Variable"],
            ["Variable","ID","VariMore"],
            ["VariMore",""],
            ["VariMore","LB","Exp","RB"],
            ["VariMore","END_PROGRAM","FieldVar"],
            ["FieldVar","ID","FieldVarMore"],
            ["FieldVarMore",""],
            ["FieldVarMore","LB","Exp","RB"],
            ["CmpOp","ST"],
            ["CmpOp","EQUAL"],
            ["AddOp","PLUS"],
            ["AddOp","MINUS"],
            ["MultOp","MULTIPLY"],
            ["MultOp","SLASH"],
            # ???????????????
            ["Exp","CHARS"]
        ]

TERMINAL = 0
NON_TERMINAL = 1
# ????????????????????????
TYPE = {"#":TERMINAL}

s = set()
# ???????????????????????????set??????????????????????????????????????????????????????
for grammar in G:
    for w in grammar:
        s.add(w)
# ?????????????????????????????????????????????????????????,????????????????????????
for word in s:
    if word == word.upper():
        TYPE[word] = TERMINAL
    else:
        TYPE[word] = NON_TERMINAL

start = "Program"
first = get_first(TYPE,G)
follow = get_follow("",TYPE,G,first)
predict = get_predict(G,first,follow)



terminal,non_terminal,predict_table = get_predict_table(G,TYPE,predict)


# ???????????????predict??????????????????
print("get the predict_table")
for key in predict_table.keys():
    print(key," :",predict_table[key])

print("finish")


# # print("the first is :",first["DeclarePart"])
# # print("the follow is :",predict_table["ProcDecPart"])

# print("the predict is :",predict_table["ProcDecMore"])
# # print(len(predict_table["OtherFactor"]))
# print("the follow is :",follow["ProcDec"])
# print("first :",first["ProcDec"])

def parse(path):
    # ??????????????????????????????????????????
    f = open(path,"r")
    # ??????????????????token??????
    Token_List = [Token.unserilze(i.strip()) for i in f.readlines()]
    
    q = Queue()
    # ????????????????????????
    for token in Token_List:
        q.put(Node(token.type,token.semantic))
    q.put(Node("#","#"))
    start = Node("Program","Program")
    parser = Parser_Tree(G,TYPE,predict_table,start,q)
    parser.parse()

    start.dfs()

    start.drawTree()
    pass

if __name__ == '__main__':
    parse(sys.argv[1])

    # ????????????????????????
