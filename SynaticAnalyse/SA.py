import pickle
import sys
sys.path.append("..")

from Parser.RecursiveParser import TreeNode


class SA:
    def __init__(self,tree:TreeNode):        
        self.ptree = tree
        self.simpleTable = []
        self.useTable = []
    
    def dfs(self):
        self.ptree.dfs()
    
    def createSimpleTable(self):
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
                elif root.is_id and root.name not in self.simpleTable:
                    raise TypeError("Use Variable:"+root.name+" before Declaration")
                for i in root.child:
                    symbolSearchDFS(i)

            # if root.is_id == True:
            #     self.simpleTable.append(root.name)
            # for i in root.child:
            #     symbolSearchDFS(i)
        
        symbolSearchDFS(self.ptree)
        print(self.simpleTable)

    


if __name__=="__main__":
    
    f = open("../Parser/temp.tok.ptree", 'rb')
    d = pickle.load(f)
    a = SA(d)
    a.createSimpleTable()
    
    
        
        