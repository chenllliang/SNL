from Tokenizer.Tokenizer import tokenize

from Parser.RecursiveParser import RecurParse

from SynaticAnalyse.SA import SA

from LL1.parse import parse

import pickle

if __name__=="__main__":
    import sys
    tokenize(sys.argv[1])
    # use recursive one
    RecurParse(sys.argv[1]+".tok")
    
    # use ll1
    
    f = open(sys.argv[1]+".tok.ptree", 'rb')
    d = pickle.load(f)
    a = SA(d)
    a.createBidiTree()

    # LL1语法分析
    parse(sys.argv[1]+".tok")
