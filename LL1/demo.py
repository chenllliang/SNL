import LL1Parser
from LL1Parser import Node,Parser,Parser_Tree

# 1对应非终极符，0对应终极符
TYPE = {"E":1,"T":1,"E'":1,"+":0,"F":1,"*":0,"T'":1,"i":0,"(":0,")":0,"":0,"#":0}
# 所有的文法规则
G = [
    ["E","T","E'"],
    ["E'","+","T","E'"],
    ["E'",""],
    ["T","F","T'"],
    ["T'","*","F","T'"],
    ["T'",""],
    ["F","i"],
    ["F","(","E",")"]
]
start = "E"

# 再换一组测试
# TYPE = {"S":1,"A":1,"B":1,"a":0,"b":0,"c":0,"":0}
# G = [
#     ["S","A","B","c"],
#     ["A","a"],
#     ["A",""],
#     ["B","b"],
#     ["B",""]
# ]
# start = "S"

if __name__ == '__main__':
    from queue import Queue

    first = LL1Parser.get_first(TYPE,G)
    print("the first is :",first)

    follow = LL1Parser.get_follow(start,TYPE,G,first)
    print("the follow is :",follow)

    predict = LL1Parser.get_predict(G,first,follow)
    print("the predict is :",predict)

    terminal,non_terminal,predict_table = LL1Parser.get_predict_table(G,TYPE,predict)
    print("the predict_table is :",predict_table)

    s = "i+i*i#"
    a = Queue()
    for l in s:
        a.put(l)
    seq = Queue()
    for l in a.queue:
        seq.put(Node(l,l))

    parser = Parser(G,TYPE,predict_table,start,a)
    parser.parse()

    st = Node(start,None)

    parse_tree = Parser_Tree(G,TYPE,predict_table,st,seq)
    parse_tree.parse()

    st.dfs()