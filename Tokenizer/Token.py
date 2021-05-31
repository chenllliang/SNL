from enum import Enum



class Token:
    def __init__(self,id:int,t_type:str,semantic=None):
        self.id = id
        self.type = t_type
        self.semantic = semantic

    def __str__(self):
        return "id:"+str(self.id)+" type:"+str(self.type)+" value:"+str(self.semantic)


if __name__ == '__main__':
    a = Token(0,"ADD",None)
    print(a)
