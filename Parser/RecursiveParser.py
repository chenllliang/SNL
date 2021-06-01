import sys

sys.path.append("..")

import json
from Tokenizer.Token import Token

Token_List = []
i = 0


class TreeNode:
    def __init__(self, token):
        self.name = token
        self.child = []


    def dfs(self):
        print(self.name)
        for i in self.child:
            i.dfs()




def RecurParse(path):
    global i, Token_List
    f = open(path, "r")
    Token_List = [Token.unserilze(i.strip()) for i in f.readlines()]
    root = TreeNode("ROOT")
    Program(root)

    root.dfs()
    print("Done")



def Program(node:TreeNode):
    ProgramHead(node)
    DeclarePart(node)
    ProgramBody(node)
    match("END_PROGRAM",node)



def ProgramHead(node:TreeNode):
    match("PROGRAM",node)
    ProgramName(node)


def ProgramName(node:TreeNode):
    match("ID",node)


def DeclarePart(node:TreeNode):
    TypeDecpart(node)
    VarDecpart(node)
    ProcDecpart(node)


def TypeDecpart(node:TreeNode):
    pass


def VarDecpart(node:TreeNode):
    pass


def ProcDecpart(node:TreeNode):
    pass


def ProgramBody(node:TreeNode):
    pass


def match(strings: str,node:TreeNode):
    global i, Token_List

    if Token_List[i].type == strings:
        node.child.append(TreeNode(strings))
        i += 1
        return
    else:
        raise TypeError(strings)


if __name__ == "__main__":
    rules = json.load(open("rules.json"))
    RecurParse("temp.tok")
