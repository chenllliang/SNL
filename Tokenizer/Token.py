from enum import Enum



class Token:
    def __init__(self,id:int,t_type:str,semantic=None):
        self.id = id
        self.type = t_type
        self.semantic = semantic

    def __str__(self):
        return "id:"+str(self.id)+" type:"+str(self.type)+" value:"+str(self.semantic)

    @staticmethod
    def unserilze(data):
        idd,typee,valuee = data.split(" ")
        return Token(int(idd.split(":")[1]),typee.split(":")[1],valuee.split(":")[1])


if __name__ == '__main__':
    a = Token.unserilze("id:2 type:ID value:v3")
    print(a)
