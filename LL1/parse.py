from queue import Queue
import LL1Parser
from LL1Parser import Node,Parser_Tree
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
            ["ProcDecMore","ProcDeclaration"],
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
            # 新加的规则
            ["Exp","CHARS"]
        ]

TERMINAL = 0
NON_TERMINAL = 1
# 记录所有的种类，
TYPE = {"#":TERMINAL}

s = set()
# 将所有的符号都放进set集合中，然后判断是终极符还是非终极符
for grammar in G:
    for w in grammar:
        s.add(w)
# 如果大写跟原本一样，那么就说明是终极符,否则则是非终极符
for word in s:
    if word == word.upper():
        TYPE[word] = TERMINAL
    else:
        TYPE[word] = NON_TERMINAL

start = "Program"
first = LL1Parser.get_first(TYPE,G)
follow = LL1Parser.get_follow("",TYPE,G,first)
predict = LL1Parser.get_predict(G,first,follow)



terminal,non_terminal,predict_table = LL1Parser.get_predict_table(G,TYPE,predict)


# 打印对应的predict集，是相同的
print("get the predict_table")
for key in predict_table.keys():
    print(key," :",predict_table[key])

print("finish")


# print("the first is :",first["DeclarePart"])
# print("the follow is :",predict_table["ProcDecPart"])

print("the predict is :",predict_table["StmList"])
# print(len(predict_table["OtherFactor"]))
print("the follow is :",follow["StmList"])
print("first :",first["FI"])

def parse(path):
    # 打开已经进行完语法分析的文件
    f = open(path,"r")
    # 获取解析后的token集合
    Token_List = [Token.unserilze(i.strip()) for i in f.readlines()]
    
    q = Queue()
    # 把对应的结果变成
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

    # 对于输入进行处理
