import json

Token_list = []

stack = list()

TYPE = {}

grammar = [None,
            ["Program","ProgramHead","DeclarePart","ProgramBody","."],];

# 计算对应文法中所有的First集

First = {}

# 计算对应文法中的Follow集

Follow = {}

# 计算所有文法的Predict集

Predict = {}

def get_first():


# class TreeNode():

