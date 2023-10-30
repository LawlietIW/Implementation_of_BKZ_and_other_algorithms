import numpy as np


def sub_RED(k,l, Bm, Mym):
    if abs(Mym[k,l]) <= 0.5:
        return Bm, Mym   #Probably not needed
    
    q = np.floor(0.5 + Mym[k,l])   #round to nearest integer
    Bm[k] = Bm[k] - q*Bm[l]
    Mym[k,l] = Mym[k,l] - q
    for i in range(l):
        Mym[k,i] = Mym[k,i] - q*Mym[l,i]
    return Bm,  Mym 


def step2(k, Bm, B_gs, Mym, B_norms, epsilon = 0.05):
    """Incremental Gram-Schmidt"""
    for j in range(k):
        if B_norms[j] > epsilon:
            Mym[k,j] = np.inner(Bm[k],B_gs[j])/B_norms[j]
        else:
            Mym[k,j] = 0
    print("Thing in sum:", [Mym[k,j]*B_gs[j] for j in range(k)])
    B_gs[k] = Bm[k] - sum([Mym[k,j]*B_gs[j] for j in range(k)])
    B_norms[k] = np.linalg.norm(B_gs[k])**2
    return B_gs, Mym, B_norms


def swapG(k, kmax, Bm, Mym, B_norms, epsilon = 0.05):
    # print("Before:", Bm)
    Bm[[k-1,k]] = Bm[[k, k-1]]
    # print("After:", Bm)
    if k > 1:
        for j in range(k-1):
            tempswap = Mym[k-1,j]  #Only number so don't need copy
            Mym[k-1,j] = Mym[k,j]
            Mym[k,j] = tempswap

    mu = Mym[k,k-1]
    B = B_norms[k] + mu**2*B_norms[k-1]
    # print(B)
    if B < epsilon:
        print("Before:" , B_norms)
        B_norms[[k-1,k]] = B_norms[[k,k-1]]
        print("After:", B_norms)
        for i in range(k+1,kmax + 1):
            t = Mym[i,k] 
            Mym[i,k] = Mym[i,k-1]
            Mym[i,k-1] = t
    elif B_norms[k] <= epsilon and mu != 0:
        B_norms[k-1] = B
        Mym[k,k-1] = 1/mu
        for i in range(k+1,kmax + 1):
            Mym[i,k-1] = Mym[i,k-1]/mu
    elif B_norms[k] != 0:
        t = B_norms[k-1]/B
        Mym[k,k-1] = mu*t
        B_norms[k] = B_norms[k]*t
        B_norms[k-1] = B
        for i in range(k+1,kmax + 1):
            t = Mym[i,k]
            Mym[i,k] = Mym[i,k-1] - mu*t
            Mym[i,k-1] = t + Mym[k,k-1]*Mym[i,k]
    return Bm, Mym, B_norms


def step3(k, kmax, Bm, Mym, B_norms, delta = 3/4):
    """Test LLL condition"""
    # print("Mym before: ")
    # print(Mym)
    Bm,  Mym = sub_RED(k,k-1, Bm, Mym)
    print("k:", k)
    print("kmax:", kmax)
    print("Bm in 3: ")
    print(Bm)
    print("Mym in 3: ")
    print(Mym)

    if B_norms[k] < (delta - Mym[k,k-1]**2) * B_norms[k-1]:
        print("Swap")
        Bm, Mym, B_norms = swapG(k, kmax, Bm, Mym, B_norms)
        print("Bm after swap: ")
        print(Bm)
        print("Mym after swap: ")
        print(Mym)
        k = max(1,k-1)
        k, Bm, Mym, B_norms = step3(k, kmax, Bm, Mym, B_norms, delta)
    else:
        print("Reduce")
        for l in reversed(range(0,k-1)):
            Bm, Mym = sub_RED(k,l, Bm, Mym)
        k += 1
        print("Bm after reduce: ")
        print(Bm)
        print("Mym after reduce: ")
        print(Mym)
    return k, Bm, Mym, B_norms

def main_LLL(Bm, delta = 3/4):
    """
    Main LLL algorithm
    """
    r,c = Bm.shape
    k = 1
    kmax = 0
    B_gs = np.zeros((r,c))
    B_gs[0] = Bm[0]
    Mym = np.zeros((r,r))
    # print("B_gs:")
    # print(B_gs)
    B_norms = np.zeros(r)
    B_norms[0] = np.linalg.norm(Bm[0])**2

    while k < r:
        # print("k:", k)
        # print("kmax:", kmax)
        # print("Bm:")
        # print(Bm)
        # print("B_gs:")
        # print(B_gs)

        if k > kmax:
            print()
            print()
            print("Step 2")
            print("Bm before: ")
            print(Bm)
            print("B_gs before: ")
            print(B_gs)
            print("Mym before: ")
            print(Mym)
            kmax = k
            B_gs, Mym, B_norms = step2(k, Bm, B_gs, Mym, B_norms)
        # print("B_gs after:")
        # print(B_gs)
        print("Mym after:")
        print(Mym)
        """Step 3"""
        print()
        print()
        print("Step 3")
        # B_gs[[k-1,k]] = B_gs[[k, k-1]]
        k, Bm, Mym, B_norms = step3(k, kmax, Bm, Mym, B_norms, delta)
        
    return Bm
            

if __name__ == "__main__":
    # Bm = np.random.randint(100, size=(3, 3))
#     Bm = np.array([[20, 16, 23, 91, 98, 11, 94, 68,  3],
#  [48, 63, 28,  2,  1, 31, 96, 92,  2],
#  [16, 29,  5, 38, 48, 75, 16, 47, 88],
#  [34, 95, 98, 19,  2, 13, 24, 78, 32],
#  [65, 23,  6, 34, 87, 28, 74, 33, 24],
#  [93, 26, 78, 22, 19, 43, 10, 48, 58],
#  [74, 33, 84, 78, 13, 65, 71, 12, 32],
#  [51, 62, 74, 93, 91, 14, 89, 43, 97],
#  [90,  7, 58, 31, 68, 28, 28, 29, 38]])
    Bm = np.array([[34, 61, 20],
 [72, 91, 15],
 [22, 83, 47]])
    print("Bm: ")
    print(np.array2string(Bm, separator=', '))
    LLL = main_LLL(Bm)
    print("LLL:")
    print(LLL)



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
