class x:
    def __init__(self,data) -> None:
        self.val = data
    
    def get(self):
        return self.val
class y:
    def __init__(self,listt) -> None:
        self.list = []
        for data in listt:
            self.list.append(x(data))
        
        for data in self.list:
            print(data.get())


ls = [1,2,4,4,5]

lis = y(ls)
