import os
from enum import Enum
from sys import argv
from Token import Token
import string


class STATES(Enum):
    START = 0
    INASSIGN = 1
    INID = 2
    INNUM = 3
    INCHAR = 4
    INRANGE = 5
    DONE = 6


# tokens feature
letters = {i for i in string.ascii_letters}
digits = {str(i) for i in range(10)}
uni_delimiters = {'+': 'PLUS', '-': 'MINUS', '*': 'MULTIPLY', '/': 'SLASH',
                  '<': 'ST', '>': 'LT', '=': 'EQUAL',
                  '(': 'LP', ')': 'RP', '[': 'LB', ']': 'RB',
                  ';': 'SEMICOLON', ',': 'COMMA'}
bi_delimeter = {":=": "ASSIGN"}
list_range = {"..": "RANGE"}
char = {"\'": "CHARS"}
end = {".": "END_PROGRAM"}
error = {"ERROR": "error"}
keep_words_value = {"program", "procedure", "type", "var", "if", "then", "else", "finally", "while", "do", "endwh",
                    "begin", "end", "read", "write", "array", "of", "record", "return","integer","char"}
keey_words = {i: i.upper() for i in keep_words_value}


def tokenize(file_path):
    tokenlist = []
    cleanText(file_path)
    f = open(file_path + ".tmp", "rb")
    state = STATES.START
    token_ids = 0
    token_value = ""
    while 1:
        i = f.read(1).decode()
        if state == STATES.START:
            if i == " ":
                continue

            if isChar(i):
                state = STATES.INID
            if isNumber(i):
                state = STATES.INNUM
            if isUniDelimiter(i):
                # UniDelimiter token added
                tokenlist.append(Token(token_ids, uni_delimiters[i], None))
                token_ids += 1
                continue
            if i == ":":
                state = STATES.INASSIGN
            if i == ".":
                state = STATES.INRANGE
            if i == "\'":
                state = STATES.INCHAR

            token_value += i

        elif state == STATES.INID:
            if isChar(i) or isNumber(i):
                token_value += i
            else:
                id_type, id_value = getKeepWord(token_value)
                tokenlist.append(Token(token_ids, id_type, id_value))
                token_ids += 1
                token_value = ""
                state = STATES.START
                f.seek(-1, 1)

        elif state == STATES.INNUM:
            if isNumber(i):
                token_value += i
            else:
                tokenlist.append(Token(token_ids, "NUMBER", token_value))
                token_ids += 1
                token_value = ""
                state = STATES.START
                f.seek(-1, 1)

        elif state == STATES.INASSIGN:
            if i != "=":
                raise TypeError("unexpected symbol " + i + " in " + str(state))
            else:
                tokenlist.append(Token(token_ids, "ASSIGN", None))
                token_ids += 1
                token_value = ""
                state = STATES.START

        elif state == STATES.INRANGE:
            if i != ".":
                tokenlist.append(Token(token_ids, "END_PROGRAM", None))
            elif i == ".":
                tokenlist.append(Token(token_ids, "RANGE", None))

            token_ids += 1
            token_value = ""
            state = STATES.START

        elif state == STATES.INCHAR:
            if isNumber(i) or isChar(i):
                token_value += i

            elif i == "\'":
                token_value += i
                tokenlist.append(Token(token_ids, "CHARS", token_value))
                token_ids += 1
                token_value = ""
                state = STATES.START

        elif state == STATES.INNUM:
            if isNumber(i):
                token_value += i

            else:
                tokenlist.append(Token(token_ids, "NUMBER", token_value))
                token_ids += 1
                token_value = ""
                state = STATES.START
                f.seek(-1, 1)

        if not i:
            break

    with open(file_path + ".tok", "w") as f:
        for i in tokenlist:
            print(i)
            f.write(str(i) + "\n")


def cleanText(path):
    # remove comment, redudant space , newline, tab
    f = open(path, "r")
    tmp = open(path + ".tmp", "w")

    keep_reading = 1
    continue_space = 0
    comment_state = 0
    while keep_reading:
        i = f.read(1)
        if len(i) == 0:
            break

        if comment_state and i != "}":
            continue
        elif i == "}":
            comment_state = 0
            continue

        if i == "{":
            comment_state = 1
            continue

        if i in [" ", "\t", "\r", "\n"]:
            if not continue_space:
                tmp.write(" ")
                continue_space = 1
                continue
            else:
                continue
        else:
            continue_space = 0

        tmp.write(i)
    tmp.close()


def isChar(char:str):
    return char in letters


def isNumber(char:str):
    return char in digits


def isUniDelimiter(char:str):
    return char in uni_delimiters.keys()

def getKeepWord(name:str):
    if name in keep_words_value:
        return keey_words[name], None
    else:
        return "ID", name


def left_bracket():
    pass


if __name__ == '__main__':
    import sys

    tokenize(sys.argv[1])
