import math

n = 1, 2, 3, 4, 5
area = []

def calcir(r):
    radpow = r * r
    return math.pi * radpow

for i in n :
    area.append(calcir(i))

area.pop(0)
area.append(10)
print (sum(area))

grades = {"nai":69, "ian":96}
print(grades["nai"])



