from utility import *
#test Marblebag_random
# --------------------------------------------------
print("Marblebag_random")
print("--------------------")
mybag = [1, 2, 3, 4, 5, 6, 7, 8]
classtest1 = Marblebag_random(mybag)

for i in range(len(mybag)):
    print(i + 1)
    print(classtest1.draw())
    print()

#test Progressive_random
# --------------------------------------------------
print("Progressive_random")
print("--------------------")
classtest2 = Progressive_random()

for i in range(10):
    print(i + 1)
    print(classtest2.draw())
    print()

#test Fixed_limit_random
# --------------------------------------------------
print("Fixed_limit_random")
print("--------------------")
classtest3 = Fixed_limit_random()

for i in range(10):
    print(i + 1)
    print(classtest3.draw())
    print()

#test Predetermination_random:
# --------------------------------------------------
print("Predetermination_random")
print("--------------------")
classtest4 = Predetermination_random()
for i in range(10):
    print(i + 1)
    print(classtest4.draw())
    print()