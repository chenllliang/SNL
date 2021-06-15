
# 1.如果X是终结符，则FIRST(X) = {X}.
# 2.如果X是非终结符 ，且有产生式 X → a… 则把a加入到FIRST集合中.
# 若 X → ε也是其中一条产生式，则把ε也加入到FIRST集合中.
# 3.如果X是非终结符，且 X → Y… 是一条产生式，其中Y是非终结符，那么则把FIRST(Y) \ {ε}（即FIRST集合去除ε）加入到FIRST(X)中.
# 更复杂些的，对于产生式 X → Y1 Y2…Yi-1 Yi…Yk ，其中Y1，…，Yi-1都是非终结符：
# ① 对于任意的j，满足 1 <= j <= i-1 ，且FIRST(Yj)都含有ε，则把
# FIRST(Yi) \ {ε} 加入到FIRST(X)中.
# ② 对于任意的p，满足 1 <= p <= k ，且FIRST(Yp)都含有ε，则把
# ε加入到FIRST(X)中.


# 根据文法求First集
def get_first(TYPE,G):
    first = {}
    # 首先所有的终极符对应的first集一定是自身，所以先加入进去
    for key in TYPE.keys():
        if not TYPE[key]:
            first[key] = [key]
        else:
            first[key] = []
    # 之后开始更新First集，因为不确定先后顺序，因此只要有改变就在结束后重新遍历

    flag = True
    # 每次如果First集有更新，就置flag为True，下次继续遍历
    while flag:
        flag = False
        for grammar in G:
            # 要求的一定是第一个
            need = grammar[0]
            # 后面是推导
            # 如果会推出空串，那么则将空串加入,如果不在的话，则更新flag
            if grammar[1] == "" and "" not in first[need]:
                first[need].append("")
                flag = True;
            # 如果不是空串，后面跟着终极符，则直接加入,如果不在first中，则更新flag
            elif not TYPE[grammar[1]] and grammar[1] not in first[need]:
                
                first[need].append(grammar[1])
                flag = True
                pass
            # 如果不是空串或者终极符，那么就需要根据后面的非终极符来进行更新了
            else:
                # 依次遍历后面的，如果后面的非终极符中含有空串，则继续下一个符号
                idx = 1
                while idx < len(grammar):
                    has_next = False
                    tmp = grammar[idx]
                    for p in first[tmp]:
                        # 如果可以推出空的话，那么就遍历下一个符号的first集
                        if p == "":
                            idx += 1
                            has_next = True
                        # 如果推出的不在first中的话 那么就加入
                        elif p not in first[need]:
                            first[need].append(p)
                            flag = True
                    # 如果遍历的非终极符不会有空，则直接break
                    if not has_next:
                        break
                # 这里要加上，如果前面都有可能是空，则自己要加上空
                if idx == len(grammar) and "" not in first[need]:
                    first[need].append("")
                    flag = True
    return first

# 根据文法求Follow集

def get_follow(start,TYPE,G,FIRST):
    follow = {}
    check_list = [key for key in TYPE.keys() if TYPE[key]]
    # 对所有非终极符进行初始化
    for key in check_list:
        if TYPE[key]:
            follow[key] = []
    follow[start] = ["#"]

    flag = True
    # 还是不断更新 一直到收敛为止
    while flag:
        flag = False
        # 对每个非终极符，在每个文法中找
        for key in check_list:
            for grammar in G:
                if key in grammar and grammar[0] != key:
                    # 如果该非终极符不在推导式左边，则开始求其follow集
                    # 这样只能得到最近的，但是有可能一个表达式中有多个相同的key，比如 THEN StmList ELSE StmList FI
                    idxs = [i for i in range(len(grammar)) if grammar[i] == key]
                    # if key == "StmList":
                    #     print("the indexs are :",idxs)
                    #     print(grammar)
                    for idx in idxs:
                        need_pre = True
                        tmp = idx + 1

                        while tmp < len(grammar):
                            has_next = False
                            for f in FIRST[grammar[tmp]]:
                                # 如果后面的符号可能会推出空的话，那么就再看下一个
                                if f =="":
                                    has_next = True
                                    tmp += 1
                                # 如果对应的非终极符不在follow集里面，那么就加进去
                                elif f not in follow[key]:
                                    flag = True
                                    follow[key].append(f)
                            # 如果后面不会有空串，那么就停止
                            if not has_next:
                                need_pre = False
                                break
                        # 如果 key在推理时，可能还是会有空串，那么就加上最前面推理的follow集合
                        # if key == "" 
                        if need_pre:
                            for f in follow[grammar[0]]:
                                if not f in follow[key]:
                                    flag = True
                                    follow[key].append(f)                
    return follow

def get_predict(G,FIRST,FOLLOW):
    predict = []
    
    for grammar in G:
        idx = 1 
        l = []
        while(idx < len(grammar)):
            has_next = False
            # 遍历所有的first
            for w in FIRST[grammar[idx]]:
                if w =="":
                    has_next = True
                    idx += 1
                elif w not in l:
                    l.append(w)
            if not has_next:
                break
        # 判断后面会不会还是空,即推导式可能推出空,则加入Follow(A)
        if idx == len(grammar) and has_next == True:
            for w in FOLLOW[grammar[0]]:
                if w not in l:
                    l.append(w)
        predict.append(l)
        l = []
    
    return predict


def get_predict_table(G,TYPE,PREDICT):
    # 得到终极符和非终极符集合
    terminal = [t for t in TYPE.keys() if not TYPE[t]]
    non_terminal = [t for t in TYPE.keys() if TYPE[t]]
    table = {}
    # 用非终极符来构建表
    for t in non_terminal:
        table[t] = {}
        for idx,grammar in enumerate(G):
            # 如果这个文法是关于这个非终极符的解析，则加入
            if t == grammar[0]:
                for pre in PREDICT[idx]:
                    table[t][pre] = idx
    
    return terminal,non_terminal,table

class Node:
    def __init__(self,type,value) :
        self.type = type
        self.value = value
        self.children = []

    def dfs(self, depth=0):
        if self.type != self.value:
            print("\033[32m%s\033[0m" % ("--" * depth + self.type))
        else:
            print("--" * depth + self.type)
        for i in self.children:
            i.dfs(depth + 1)


class Parser_Tree:
    def __init__(self,G,TYPE,PREDICT_TABLE,start,seq):
        self.G = G
        self.TYPE = TYPE
        self.predict_table = PREDICT_TABLE
        self.stack = []
        self.stack.append(Node("#","#"))
        self.stack.append(start)
        self.seq = seq

    def parse_once(self):
        temp = self.stack[-1]
        word = self.seq.queue[0]

        # 开始解析

        # 如果类型是终极符，那么进行匹配
        if not self.TYPE[temp.type]:
            if temp.type == word.type:
                temp.value = word.value
                self.stack.pop()
                self.seq.get()
            else:
                assert("error!")
        # 如果是非终极符，那么通过Predict_table来找应该用什么文法进行替换
        else:
            # 如果在表中有对应的信息，则直接替换
            if word.type in self.predict_table[temp.type]:
                grammar = self.G[self.predict_table[temp.type][word.type]][1:]
                self.stack.pop()
                grammar.reverse()
                for k in grammar:
                    if k != "":
                        node = Node(k,k)
                        self.stack.append(node)
                        temp.children.append(node)
            # 如果表中没有信息，则报错
            else:
                assert("error!")
    
    def parse(self):


        while self.stack and self.seq.queue:
            stack = []
            for s in range(len(self.stack)-1,-1,-1):
                stack.append(self.stack[s].type)
            print("the stack is :",stack)
            l = [k.type for k in self.seq.queue]
            print("the sequence is :",l)
            self.parse_once()
        
        if not self.stack and not self.seq.queue:
            print("Succeed!")
        else:
            assert("error!")
            


# 设计类进行分析
class Parser:
    def __init__(self,G,TYPE,PREDICT_TABLE,start,seq):
        self.G = G
        self.TYPE = TYPE
        self.predict_table = PREDICT_TABLE
        self.stack = ["#"]
        self.stack.append(start)
        self.seq = seq
    
    def parse(self):
        while self.stack and self.seq.queue:
            print("the stack is :",self.stack)
            print("the sequence is :",self.seq.queue)
            self.parse_once()
        # 如果都是空了，则表示匹配正确
        if not self.stack and not self.seq.queue:
            print("Succeed!")
        else:
            assert("error!")

    def parse_once(self):
        temp = self.stack[-1]
        word = self.seq.queue[0]

        # 开始解析

        # print("the temp is :",temp)
        # print("the word is :",word)

        # 如果从符号栈中得到的是终极符的，那么直接进行匹配
        if not self.TYPE[temp]:
            # 匹配成功则直接去掉
            if temp == word:
                self.stack.pop()
                self.seq.get()
            # 匹配失败则报错
            else:
                assert("error!")
        # 如果是非终极符，则通过Predict_table，找应该用哪个文法进行替换
        else:
            # 如果在表中有对应的信息，则直接替换
            if word in self.predict_table[temp]:
                grammar = self.G[self.predict_table[temp][word]][1:]
                self.stack.pop()
                grammar.reverse()
                for k in grammar:
                    if k != "":
                        self.stack.append(k);
            # 否则报错
            else:
                assert("error!")