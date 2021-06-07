import sys
from graphviz import Digraph
import pickle


sys.path.append("..")

import json
from Tokenizer.Token import Token

Token_List = []
i = 0


class TreeNode:
    def __init__(self, token, types, is_id = False):
        self.name = token
        self.type = types
        self.is_id = is_id
        self.child = []

    def append(self, x):
        self.child.append(x)

    def dfs(self, depth=0):
        if self.type == "T" and self.is_id== False:
            print("\033[32m%s\033[0m" % ("--" * depth + self.name))
         
        elif self.type == "T" and self.is_id== True:
            print("\033[31m%s\033[0m" % ("--" * depth + self.name))

        else:
            print("--" * depth + self.name)
        for i in self.child:
            i.dfs(depth + 1)
    
    def serilaize(self,file_name):
        f = open(file_name, 'wb')
        pickle.dump(self, f)

    def outputSymbolList(self):
        pass

    def drawTree(self):
        graphviz_scripts = ""
        cur_node_id = 0

        g = Digraph('测试图片')
        # g.edge('a','b',color='green')
        # g.view()

        node_queue = []
        node_queue.append([self,"#"])

        while len(node_queue)!=0:
            for i in node_queue[0][0].child:
                if i.type=="T":
                    g.node(name=i.name+"_"+str(cur_node_id),color='green')
                else:
                    g.node(name=i.name+"_"+str(cur_node_id),color='black')
                g.edge(node_queue[0][0].name+"_"+node_queue[0][1],i.name+"_"+str(cur_node_id))
                node_queue.append([i,str(cur_node_id)])
                cur_node_id += 1
            node_queue = node_queue[1:]
        
        g.view(filename="temp.jpg")
                
            


def RecurParse(path):
    global i, Token_List
    f = open(path, "r")
    Token_List = [Token.unserilze(i.strip()) for i in f.readlines()]
    root = TreeNode("ROOT", "NT")
    root.append(Program())

    root.dfs()

    root.drawTree()
    root.serilaize(path+".ptree")


def Program():
    cur_node = TreeNode("Program", "NT")
    cur_node.append(ProgramHead())
    cur_node.append(DeclarePart())
    cur_node.append(ProgramBody())
    cur_node.append(match("END_PROGRAM"))

    return cur_node


def ProgramHead():
    cur_node = TreeNode("ProgramHead", "NT")
    cur_node.append(match("PROGRAM"))
    cur_node.append(ProgramName())

    return cur_node


def ProgramName():
    cur_node = TreeNode("ProgramName", "NT")
    cur_node.append(match("ID"))

    return cur_node


def DeclarePart():
    cur_node = TreeNode("DeclarePart", "NT")
    cur_node.append(TypeDecpart())
    cur_node.append(VarDecpart())
    cur_node.append(ProcDecpart())

    return cur_node


def TypeDecpart():
    global i, Token_List
    if Token_List[i].type == "TYPE":
        cur_node = TreeNode("TypeDecpart", "NT")
        cur_node.append(TypeDec())
        return cur_node
    else:
        return TreeNode("TypeDecpart", "NT")


def TypeDec():
    cur_node = TreeNode("TypeDec", "NT")
    cur_node.append(match("TYPE"))
    cur_node.append(TypeDecList())
    return cur_node


def TypeDecList():
    cur_node = TreeNode("TypeDecList", "NT")
    cur_node.append(TypeID())
    cur_node.append(match("EQUAL"))
    cur_node.append(TypeDef())
    cur_node.append(match("SEMICOLON"))
    cur_node.append(TypeDecMore())

    return cur_node


def TypeID():
    cur_node = TreeNode("TypeID", "NT")
    cur_node.append(match("ID"))
    return cur_node


def TypeDef():
    global i, Token_List
    cur_node = TreeNode("TypeDef", "NT")
    if Token_List[i].type in ["INTEGER", "CHAR"]:
        cur_node.append(BaseType())
        return cur_node
    if Token_List[i].type == "ARRAY":
        cur_node.append(ArrayType())
        return cur_node
    if Token_List[i].type == "ID":
        cur_node.append(match("ID"))
        return cur_node


def BaseType():
    global i, Token_List
    cur_node = TreeNode("BaseType", "NT")
    cur_node.append(match(Token_List[i].type))
    return cur_node


def ArrayType():
    cur_node = TreeNode("ArrayType", "NT")
    cur_node.append(match("ARRAY"))
    cur_node.append(match("LB"))
    cur_node.append(Low())
    cur_node.append(match("RANGE"))
    cur_node.append(Top())
    cur_node.append(match("RB"))
    cur_node.append(match("OF"))
    cur_node.append(BaseType())
    return cur_node


def Low():
    cur_node = TreeNode("Low", "NT")
    cur_node.append(match("NUMBER"))
    return cur_node


def Top():
    cur_node = TreeNode("Top", "NT")
    cur_node.append(match("NUMBER"))
    return cur_node


def TypeDecMore():
    cur_node = TreeNode("TypeDecMore", "NT")
    global i, Token_List
    if Token_List[i].type == "ID":
        cur_node.append(TypeDecList())
    return cur_node


def VarDecpart():
    cur_node = TreeNode("VarDecpart", "NT")
    global i, Token_List
    if Token_List[i].type == "VAR":
        cur_node.append(VarDec())
        return cur_node
    else:
        return cur_node


def VarDec():
    cur_node = TreeNode("VarDec", "NT")
    cur_node.append(match("VAR"))
    cur_node.append(VarDecList())
    return cur_node


def VarDecList():
    cur_node = TreeNode("VarDecList", "NT")
    cur_node.append(TypeDef())
    cur_node.append(VarIdList())
    cur_node.append(match("SEMICOLON"))
    cur_node.append(VarDecMore())

    return cur_node


def VarDecMore():
    cur_node = TreeNode("VarDecMore", "NT")
    global Token_List, i
    if Token_List[i].type in ["INTEGER", "CHAR", "ARRAY", "ID"]:
        cur_node.append(VarDecList())

    return cur_node


def VarIdList():
    cur_node = TreeNode("VarIdList", "NT")
    cur_node.append(match("ID"))
    cur_node.append(VarIdMore())
    return cur_node


def VarIdMore():
    cur_node = TreeNode("VarIdMore", "NT")
    global Token_List, i
    if Token_List[i].type == "COMMA":
        cur_node.append(match("COMMA"))
        cur_node.append(VarIdList())
    return cur_node


def ProcDecpart():
    cur_node = TreeNode("ProcDecpart", "NT")
    global Token_List, i
    if Token_List[i].type == "PROCEDURE":
        cur_node.append(ProcDec())
    return cur_node


def ProcDec():
    cur_node = TreeNode("ProcDec", "NT")
    cur_node.append(match("PROCEDURE"))
    cur_node.append(ProcName())
    cur_node.append(match("LP"))
    cur_node.append(ParamList())
    cur_node.append(match("RP"))
    cur_node.append(match("SEMICOLON"))
    cur_node.append(ProcDecPart())
    cur_node.append(ProcBody())
    cur_node.append(ProcDecMore())
    return cur_node


def ProcBody():
    cur_node = TreeNode("ProcBody", "NT")
    cur_node.append(ProgramBody())
    return cur_node


def ProcDecPart():
    cur_node = TreeNode("ProcDecPart", "NT")
    cur_node.append(DeclarePart())
    return cur_node


def ProcDecMore():
    cur_node = TreeNode("ProcDecMore", "NT")
    global Token_List, i
    if Token_List[i].type == "PROCEDURE":
        cur_node.append(ProcDec())
    return cur_node


def ProcName():
    cur_node = TreeNode("ProcName", "NT")
    cur_node.append(match("ID"))
    return cur_node


def ParamList():
    cur_node = TreeNode("ParamList", "NT")
    global Token_List, i
    if Token_List[i].type in ["INTEGER", "CHAR", "ARRAY", "ID", "VAR"]:
        cur_node.append(ParamDecList())
    return cur_node


def ParamDecList():
    cur_node = TreeNode("ParamDecList", "NT")
    cur_node.append(Param())
    cur_node.append(ParamMore())
    return cur_node


def ParamMore():
    cur_node = TreeNode("ParamMore", "NT")
    global Token_List, i
    if Token_List[i].type == "SEMICOLON":
        cur_node.append(match("SEMICOLON"))
        cur_node.append(ParamDecList())
    return cur_node


def Param():
    cur_node = TreeNode("Param", "NT")
    global Token_List, i
    if Token_List[i].type == "VAR":
        cur_node.append(match("VAR"))
        cur_node.append(TypeDef())
        cur_node.append(FormList())
    else:
        cur_node.append(TypeDef())
        cur_node.append(FormList())

    return cur_node


def FormList():
    cur_node = TreeNode("FormList", "NT")
    cur_node.append(match("ID"))
    cur_node.append(FidMore())
    return cur_node


def FidMore():
    cur_node = TreeNode("FidMore", "NT")
    global Token_List, i
    if Token_List[i].type == "COMMA":
        cur_node.append(match("COMMA"))
        cur_node.append(FormList())
    return cur_node


def ProgramBody():
    cur_node = TreeNode("ProgramBody", "NT")
    cur_node.append(match("BEGIN"))
    cur_node.append(StmList())
    cur_node.append(match("END"))
    return cur_node


def StmList():
    cur_node = TreeNode("StmList", "NT")
    cur_node.append(Stm())
    cur_node.append(StmMore())
    return cur_node


def Stm():
    cur_node = TreeNode("Stm", "NT")
    global Token_List, i
    if Token_List[i].type == "IF":
        cur_node.append(ConditionalStm())
    if Token_List[i].type == "WHILE":
        cur_node.append(LoopStm())
    if Token_List[i].type == "READ":
        cur_node.append(InputStm())
    if Token_List[i].type == "WRITE":
        cur_node.append(OutputStm())
    if Token_List[i].type == "ID":
        cur_node.append(match("ID"))
        cur_node.append(AssCall())
    return cur_node


def StmMore():
    cur_node = TreeNode("StmMore", "NT")
    global Token_List, i
    if Token_List[i].type == "SEMICOLON":
        cur_node.append(match("SEMICOLON"))
        cur_node.append(StmList())
    return cur_node


def ConditionalStm():
    cur_node = TreeNode("ConditionalStm", "NT")
    cur_node.append(match("IF"))
    cur_node.append(RelExp())
    cur_node.append(match("THEN"))
    cur_node.append(StmList())
    cur_node.append(match("ELSE"))
    cur_node.append(StmList())
    cur_node.append(match("FI"))

    return cur_node


def LoopStm():
    cur_node = TreeNode("LoopStm", "NT")
    cur_node.append(match("WHILE"))
    cur_node.append(RelExp())
    cur_node.append(match("DO"))
    cur_node.append(StmList())
    cur_node.append(match("ENDWH"))

    return cur_node


def InputStm():
    cur_node = TreeNode("InputStm", "NT")
    cur_node.append(match("READ"))
    cur_node.append(match("LP"))
    cur_node.append(Invar())
    cur_node.append(match("RP"))

    return cur_node


def Invar():
    cur_node = TreeNode("Invar", "NT")
    cur_node.append(match("ID"))
    return cur_node


def OutputStm():
    cur_node = TreeNode("OutputStm", "NT")
    cur_node.append(match("WRITE"))
    cur_node.append(match("LP"))
    cur_node.append(Exp())
    cur_node.append(match("RP"))

    return cur_node


def ReturnStm():
    cur_node = TreeNode("ReturnStm", "NT")
    cur_node.append(match("RETURN"))

    return cur_node


def AssCall():
    cur_node = TreeNode("AssCall", "NT")
    global Token_List, i
    if Token_List[i].type == "LP":
        cur_node.append(CallStmRest())
    else:
        cur_node.append(AssignmentRest())

    return cur_node


def CallStmRest():
    cur_node = TreeNode("CallStmRest", "NT")
    cur_node.append(match("LP"))
    cur_node.append(ActParamList())
    cur_node.append(match("RP"))
    return cur_node


def ActParamList():
    cur_node = TreeNode("ActParamList", "NT")

    global Token_List, i
    if Token_List[i].type in ["LP", "NUMBER", "ID"]:
        cur_node.append(Exp())
        cur_node.append(ActParamMore())

    return cur_node


def ActParamMore():
    cur_node = TreeNode("ActParamMore", "NT")

    global Token_List, i
    if Token_List[i].type == "COMMA":
        cur_node.append(match("COMMA"))
        cur_node.append(ActParamList())
    return cur_node


def AssignmentRest():
    cur_node = TreeNode("AssignmentRest", "NT")
    cur_node.append(VariMore())
    cur_node.append(match("ASSIGN"))
    cur_node.append(Exp())

    return cur_node


def RelExp():
    cur_node = TreeNode("RelExp", "NT")
    cur_node.append(Exp())
    cur_node.append(OtherRelE())
    return cur_node


def Variable():
    cur_node = TreeNode("Variable", "NT")
    cur_node.append(match("ID"))
    cur_node.append(VariMore())
    return cur_node


def VariMore():
    cur_node = TreeNode("VariMore", "NT")
    global Token_List, i
    if Token_List[i].type == "LB":
        cur_node.append(match("LB"))
        cur_node.append(Exp())
        cur_node.append(match("RB"))

    return cur_node


def Exp():
    cur_node = TreeNode("Exp", "NT")
    cur_node.append(Term())
    cur_node.append(OtherTerm())
    return cur_node


def Term():
    cur_node = TreeNode("Term", "NT")
    cur_node.append(Factor())
    cur_node.append(OtherFactor())

    return cur_node


def OtherTerm():
    cur_node = TreeNode("OtherTerm", "NT")
    global Token_List, i
    if Token_List[i].type in ["PLUS", "MINUS"]:
        cur_node.append(AddOp())
        cur_node.append(Exp())

    return cur_node


def AddOp():
    cur_node = TreeNode("AddOp", "NT")

    global Token_List, i
    if Token_List[i].type == "PLUS":
        cur_node.append(match("PLUS"))
    else:
        cur_node.append(match("MINUS"))

    return cur_node


def Factor():
    cur_node = TreeNode("Factor", "NT")
    global Token_List, i
    if Token_List[i].type == "LP":
        cur_node.append(match("LP"))
        cur_node.append(Exp())
        cur_node.append("RP")
    if Token_List[i].type == "NUMBER":
        cur_node.append(match("NUMBER"))
    if Token_List[i].type == "ID":
        cur_node.append(Variable())

    return cur_node


def OtherFactor():
    cur_node = TreeNode("OtherFactor", "NT")

    global Token_List, i
    if Token_List[i].type in ["MULTIPLY", "SLASH"]:
        cur_node.append(MultOp())
        cur_node.append(Term())

    return cur_node


def MultOp():
    cur_node = TreeNode("MultOp", "NT")

    global Token_List, i
    if Token_List[i].type == "MULTIPLY":
        cur_node.append(match("MULTIPLY"))
    else:
        cur_node.append(match("SLASH"))

    return cur_node


def CmpOp():
    cur_node = TreeNode("CmpOp", "NT")
    global Token_List, i
    if Token_List[i].type == "ST":
        cur_node.append(match("ST"))
    elif Token_List[i].type == "LT":
        cur_node.append(match("LT"))
    else:
        cur_node.append(match("EQUAL"))

    return cur_node


def OtherRelE():
    cur_node = TreeNode("OtherRelE", "NT")
    cur_node.append(CmpOp())
    cur_node.append(Exp())
    return cur_node


def match(strings: str):
    global i, Token_List

    if Token_List[i].type == strings:
        semantics = Token_List[i].semantic
        i += 1
        if semantics != "None" and strings=="ID":
            return TreeNode(semantics, "T",True)
        elif semantics != "None":
            return TreeNode(semantics, "T",False)
        else:
            return TreeNode(strings, "T")
    else:
        raise TypeError("ERROR at token id:" + str(Token_List[i].id) + " Expected:" + strings)


if __name__ == "__main__":

    import sys
    RecurParse(sys.argv[1])

    # f = open(sys.argv[1]+".ptree", 'rb')
    # d = pickle.load(f)
    # d.dfs()



