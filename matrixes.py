import numpy as np 

A = np.array([
    [1, 2, 3],
    [11, 12, 13],
    [11, 22, 33]
])

B = np.array([
    [9, 8, 7]
])

res = A * B 

print(res)




C = np.array([
    [1, 2, 4],
    [2, 3, 5]
])
print(np.shape(C))

D = np.array([
    [2, 3, 4]
])

# as i expected, this does not work
# res2 = C * D 

# print(res2)
a=np.array([[2,1],[1,3]])

print(a*a)

X = np.array([
    [1,1],
    [1,-1]
])
Y = np.array([
    [2],
    [3]
])
print(X+Y)

a = 5
b = 7
c = 8
J = (a*b) + (a*c) - (b+c)
print(J)


M = (a - 1) * (b+c)
print(M)

zeros = np.zeros((1, 3))
print(zeros)