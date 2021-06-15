import pickle
import sys
sys.path.append("..")

from Parser.RecursiveParser import TreeNode



class Bidi_TreeNode:
    def __init__(self,name) -> None:
        self.name = name
        self.father = None
        self.childs = []
        self.identifiers = {}
    
    def addDeclare(self,name,types):
        # search in current level
        if name in self.identifiers.keys():
            raise TypeError("redeclare:%s error in %s"%(name,self.name))
        else:
            father_node = self.father
            while father_node!=None:
                if name in father_node.identifiers.keys():
                    raise TypeError("redeclare:%s error in %s"%(name,father_node.name))
                else:
                    father_node = father_node.father
        self.identifiers[name] = types

    def addUsage(self,name):
         # search in current level
        if name in self.identifiers.keys():
            return True
        else:
            father_node = self.father
            while father_node!=None:
                if name in father_node.identifiers.keys():
                   return True
                else:
                    father_node = father_node.father
    
        raise TypeError("%s Use before Declare! in %s"%(name,self.name))

    def addChilds(self,node):
        self.childs.append(node)
        node.father = self

    def dfs(self, depth=0):
        print("--" * depth + self.name)
        print(self.identifiers)
        for i in self.childs:
            i.dfs(depth + 1)



class SA:
    def __init__(self,tree:TreeNode):        
        self.ptree = tree
        self.simpleTable = []
        self.useTable = []
        self.symbolTable ={}
        self.bidi_tree = Bidi_TreeNode("root")
    
    def dfs(self):
        self.ptree.dfs()

    def createBidiTree(self):
        cur_node = self.bidi_tree
        proc_id = 0
        keep_jump= 0

        def cbtDFS(root:TreeNode):
            nonlocal proc_id,cur_node,keep_jump

            if root.name in ["ProcDecMore"]:
                cur_node = cur_node.father

            


            if root.name in ["Program","ProcDec"]:
                new_cbt = Bidi_TreeNode(root.name+str(proc_id))
                proc_id += 1
                cur_node.addChilds(new_cbt)
                cur_node = new_cbt

                for i in root.child:
                    cbtDFS(i)

            else:
                if root.name in ["ProgramName","FormList","VarIdList","ProgramName","TypeID"]: # 这些属于当前层声明
                    for i in root.child:
                        if i.is_id==True:
                            cur_node.addDeclare(i.name,"Variable")
                        else:
                            cbtDFS(i)
                elif root.name == "ProcName": # 这些属于上层声明
                    for i in root.child:
                        if i.is_id==True:
                            cur_node.father.addDeclare(i.name,"ProcName")
                else:
                    if root.is_id:  # 属于使用
                        cur_node.addUsage(root.name)
                    for i in root.child:
                        cbtDFS(i)

                    
        cbtDFS(self.ptree.child[0])
        self.bidi_tree.dfs()



    

    
    def createSimpleTable(self):
        cur_depth = 0
        def symbolSearchDFS(root:TreeNode):
            if root.name in ["ProcName","FormList","VarIdList","ProgramName","TypeID"]: # 这些属于声明
                for i in root.child:
                    if i.is_id==True and i.name not in self.simpleTable: # 变量没有在声明表中出现过
                        self.simpleTable.append(i.name)
                    elif i.is_id==True and i.name in self.simpleTable: # 重复声明
                        raise TypeError("Repeat Declare of Variable:"+i.name)
                    else:
                        symbolSearchDFS(i)
                
                return

            else:
                if root.is_id and root.name in self.simpleTable:
                    self.useTable.append(root.name)
                elif root.is_id and root.name not in self.simpleTable: # 使用未声明
                    raise TypeError("Use Variable:"+root.name+" before Declaration")
                for i in root.child:
                    symbolSearchDFS(i)

        
        symbolSearchDFS(self.ptree)
        print(self.simpleTable)

    


if __name__=="__main__":
    
    f = open("../Parser/temp.tok.ptree", 'rb')
    d = pickle.load(f)
    a = SA(d)
    a.createBidiTree()