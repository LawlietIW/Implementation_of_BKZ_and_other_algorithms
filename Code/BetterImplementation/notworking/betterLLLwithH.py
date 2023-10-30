import numpy as np


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


def insert(k,i, Bm, Hm):
    """Insert Bi into basis"""
    b = Bm[k]
    V = Hm[k]
    for j in reversed(range(i+1,k+1)):
        Bm[j] = Bm[j-1]
        Hm[j] = Hm[j-1]
    Bm[i] = b
    Hm[i] = V
    return Bm, Hm

def step2(k, Bm, B_gs, Mym, B_norms):
    """Incremental Gram-Schmidt"""
    B_gs[k] = Bm[k]
    for j in range(k):
        Mym[k,j] = np.inner(Bm[k],B_gs[j])/B_norms[j]
        B_gs[k] = B_gs[k] - Mym[k,j]*B_gs[j]
    B_norms[k] = np.linalg.norm(B_gs[k])**2
    if B_norms[k] == 0:
        print("Error. Bi didn't form basis")
        return "Error. Bi didn't form basis"
    return Bm, B_gs, Mym, B_norms

def step4(k, i, Bm, B_norms, Mym, B):
    """Deep LLL test"""
    if i == k:
        k += 1
        return k, i, B

    if 3/4*B_norms[i] <= B:
        B = B - Mym[k,i]**2*B_norms[i]
        i += 1
        step4(k, i, Bm, B_norms, Mym, B)

    else:
        Bm, Hm = insert(k,i, Bm, Hm)
        if i >= 1:
            k = i - 1
            B = np.linalg.norm(Bm[k])**2
            i = 1
            step4(k, i, Bm, B_norms, Mym, B)
    if i == 0:
        k = 1
    return k, i, B



def main_LLL(Bm, delta = 3/4):
    """
    Main LLL algorithm
    """
    r,c = Bm.shape
    k = 0
    B_gs = np.zeros((r,c))
    Mym = np.zeros((r,r))
    print(B_gs)
    B_norms = np.zeros(r)
    Hm = np.identity(r)

    while k < r:
        Bm, B_gs, Mym, B_norms = step2(k, Bm, B_gs, Mym, B_norms)
        if k == 0:
            k = 1
            continue   #Go to step 5

        """Initialize test"""
        for l in reversed(range(0,k-1)):
            sub_RED(k,l)
        B = np.linalg.norm(Bm[k])**2
        i = 0

        """Deep LLL test"""
        k, i, B = step4(k, i, Bm, B_norms, Mym, B)
    return Bm, Hm
            

# 

Bm = np.array([[1,2,3],[4,5,6],[7,8,9]])
main_LLL(Bm)




# print(np.linalg.norm(np.array([1,2,3]))**2)
# print(np.array([1,2,3])@np.array([1,2,3]))


















      

# def step3():
#     """Test LLL condition"""
#     sub_RED(k,k-1)
#     if B_norms[k] < (delta - Mym[k,k-1]**2)*B_norms[k-1]:
#         swap(k)
#         k = max(1,k-1)
#         go to step 3
#     else:
#         for l in reversed(range(0,k-1)):
#             sub_RED(k,l)
#         k += 1


# def swap(k, kmax, Bm, Hm, B_gs, Mym, B_norms):
#     Bm[[k-1,k]] = Bm[[k, k-1]]
#     Hm[[k-1,k]] = Hm[[k, k-1]]
#     if k > 1:
#         for j in range(k-1):
#             tempswap = Mym[k-1,j]
#             Mym[k-1,j] = Mym[k,j]
#             Mym[k,j] = tempswap

#     mu = Mym[k,k-1]
#     B = B_norms[k] + mu**2*B_norms[k-1]
#     Mym[k,k-1] = mu*B_norms[k-1]/B
#     b = B_gs[k-1]
#     B_gs[k-1] = B_gs[k] + mu*b
#     B_gs[k] = Mym[k,k-1]*B_gs[k] + (B_norms[k]/B)*b
#     B_norms[k] = B_norms[k-1]*B_norms[k]/B
#     B_norms[k-1] = B

#     for i in range(k+1,kmax):
#         t = Mym[i,k]
#         Mym[i,k] = Mym[i,k-1] - mu*t
#         Mym[i,k-1] = t + Mym[k,k-1]*Mym[i,k]



#         Mym[k,j] = np.inner(Bm[k],Bm[j])/B_norms[j]
#         Bm[k] = Bm[k] - Mym[k,j]*Bm[j]
#         B_norms[k] = np.linalg.norm(Bm[k])**2
#     return Bm, Hm, B_gs, Mym, B_norms
