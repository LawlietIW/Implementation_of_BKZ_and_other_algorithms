import numpy as np

def step2():
    kmax = k
    B_gs[k] = Bm[k]
    for j in range(k):
        Mym[k,j] = np.inner(Bm[k],B_gs[j])/B_norms[j]
        B_gs[k] = B_gs[k] - Mym[k,j]*B_gs[j]
        B_norms[k] = np.linalg.norm(B_gs[k])**2
        if B_norms[k] == 0:
            print("Error. Bi didn't form basis")
            return "Error. Bi didn't form basis"

def step3():
    """Test LLL condition"""
    sub_RED(k,k-1)
    if B_norms[k] < (delta - Mym[k,k-1]**2)*B_norms[k-1]:
        swap(k)
        k = max(1,k-1)
        go to step 3
    else:
        for l in reversed(range(0,k-1)):
            sub_RED(k,l)
        k += 1

def sub_RED(k,l, Bm, Hm, Mym):
    if abs(Mym[k,l]) <= 0.5:
        return Bm, Hm, Mym   #Probably not needed
    
    q = round(Mym[k,l])   #round to nearest integer
    Bm[k] = Bm[k] - q*Bm[l]
    Hm[k] = Hm[k] - q*Hm[l]
    Mym[k,l] = Mym[k,l] - q
    for i in range(l):
        Mym[k,i] = Mym[k,i] - q*Mym[l,i]
    return Bm, Hm, Mym


def swap(k, kmax, Bm, Hm, B_gs, Mym, B_norms):
    Bm[[k-1,k]] = Bm[[k, k-1]]
    Hm[[k-1,k]] = Hm[[k, k-1]]
    if k > 1:
        for j in range(k-1):
            tempswap = Mym[k-1,j]
            Mym[k-1,j] = Mym[k,j]
            Mym[k,j] = tempswap

    mu = Mym[k,k-1]
    B = B_norms[k] + mu**2*B_norms[k-1]
    Mym[k,k-1] = mu*B_norms[k-1]/B
    b = B_gs[k-1]
    B_gs[k-1] = B_gs[k] + mu*b
    B_gs[k] = Mym[k,k-1]*B_gs[k] + (B_norms[k]/B)*b
    B_norms[k] = B_norms[k-1]*B_norms[k]/B
    B_norms[k-1] = B

    for i in range(k+1,kmax):
        t = Mym[i,k]
        Mym[i,k] = Mym[i,k-1] - mu*t
        Mym[i,k-1] = t + Mym[k,k-1]*Mym[i,k]



        Mym[k,j] = np.inner(Bm[k],Bm[j])/B_norms[j]
        Bm[k] = Bm[k] - Mym[k,j]*Bm[j]
        B_norms[k] = np.linalg.norm(Bm[k])**2
    return Bm, Hm, B_gs, Mym, B_norms

def main_LLL(Bm, delta = 3/4):
    r,c = Bm.shape
    k = 1
    kmax = 0
    B_gs = np.zeros((r,c))
    Mym = np.zeros((r,r))
    B_gs[0] = Bm[0]
    print(B_gs)
    B_norms = np.zeros(r)
    B_norms[0] = np.linalg.norm(Bm[0])**2   #b0 * b0
    Hm = np.identity(r)

    while k < r:
        if k <= kmax:
            step3()     
        else:
            step2()
    return Bm, Hm
            

# main_LLL(np.array([[1,2,3],[4,5,6]]))

Mym = np.array([[1,2,3],[4,5,6]])
k = 1
j = 1
(0,1),(1,1)
Mym[[k-1,j],[k,j]] = Mym[[k,j],[k-1,j]]
print(Mym)




# print(np.linalg.norm(np.array([1,2,3]))**2)
# print(np.array([1,2,3])@np.array([1,2,3]))