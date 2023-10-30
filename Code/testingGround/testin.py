import numpy as np
Bm = np.array([[34, 61, 20],
 [72, 91, 15],
 [22, 83, 47]])

B_gs = np.array([[ 34.0,  61.0,  20.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])

B_norms = [Bm[0]@Bm[0]]


a = Bm[1]@B_gs[0]/B_norms[0]
print(a)



print(B_gs[0]*a)
print(Bm[1] - a * B_gs[0])
B_gs[1] = Bm[1] - a * B_gs[0]

print(B_gs)


B_norms.append(B_gs[1]@B_gs[1])

Bm[1] -= Bm[0]*2
print(Bm) 


Bm[[0,1]] = Bm[[1,0]]


print("--------------------")

print(Bm)

