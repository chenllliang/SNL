
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
                    idx = grammar.index(key)
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
                    if need_pre:
                        for f in follow[grammar[0]]:
                            if not f in follow[key]:
                                flag = True
                                follow[key].append(f)                
    return follow


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

    first = get_first(TYPE,G)
    print("the first is :",first)

    follow = get_follow(start,TYPE,G,first)
    print("the follow is :",follow)
