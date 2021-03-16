# difference between two list
def Diff(li1, li2):
    return list(set(li1)-set(li2))
 
# Driver Code
li1 = [10, 15, 20, 25, 30, 35, 40]
li2 = [25, 40, 35]
print(Diff(li2, li1))
