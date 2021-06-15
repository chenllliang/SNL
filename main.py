from Tokenizer.Tokenizer import tokenize

from Parser.RecursiveParser import RecurParse

from SynaticAnalyse.SA import SA

import pickle

if __name__=="__main__":
    import sys
    tokenize(sys.argv[1])
    RecurParse(sys.argv[1]+".tok")
    f = open(sys.argv[1]+".tok.ptree", 'rb')
    d = pickle.load(f)
    a = SA(d)
    a.createBidiTree()
