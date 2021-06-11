import pickle
import sys
sys.path.append("..")

from Parser.RecursiveParser import TreeNode


class SA:
    def __init__(self,tree:TreeNode):        
        self.ptree = tree
        self.simpleTable = []
        self.useTable = []
        self.symbolTable ={}
    
    def dfs(self):
        self.ptree.dfs()

    def createTable(self):
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
    a.createSimpleTable()