import math

l = [0,1,2,3]
w = 0
for i in l:
    t = math.sqrt(len(l))
    if i == 2:
        w = 1
    print(int(i%t), w)