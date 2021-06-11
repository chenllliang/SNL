import json

Token_list = []

stack = list()

TYPE = {}

grammar = [
            ["Program","ProgramHead","DeclarePart","ProgramBody","END_PROGRAM"],
            ["ProgramHead","PROGRAM","ProgramName"],
            ["ProgramName","ID"],
            ["DeclarePart","TypeDecpart","VarDecpart","ProcDecpart"]
            

        ]

# 计算对应文法中所有的First集

First = {}

# 计算对应文法中的Follow集

Follow = {}

# 计算所有文法的Predict集

Predict = {}


# class TreeNode():

