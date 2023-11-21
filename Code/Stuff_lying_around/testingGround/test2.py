import numpy as np

def gram_schmidt(Bm):
    """
    Computes my own QR thing. 

    Gives so Mym@B_gs is Bm.
    ------------------------------------
    Mym: (r,r)
    B_gs: (r,k)
    """
    # Bm = Bm[~np.all(Bm == 0, axis=1)]  #Removing all zero rows
    r,k = Bm.shape
    B_gs = np.zeros((r,k))
    Mym = np.zeros((r,r))
    B_gs[0] = Bm[0]
    
    # The following is just the gram schmidt algorithm
    for i in range(1,r):
        v =  Bm[i]
        for j in range(i):
            # print("Inside gram schmidt")
            # print(B_gs[j])
            if np.linalg.norm(B_gs[j]) < 0.000001:  #Cause if 0, then we get div by 0, so we just set my = 0
                my = 0
            else:
                my = np.dot(Bm[i,:],B_gs[j])/np.dot(B_gs[j],B_gs[j])
            Mym[i,j] = my
            v = v - my * B_gs[j]
        B_gs[i] = v
    return B_gs,Mym + np.diag([1]*r)  #Add the diag of 1


def pi_projection(x,b):
    """
    '''Computes the projection of x on b as a vector'''
    """
    return np.dot(x, b)/np.dot(b, b) * b

def PI(x,BGSblock):
    """
    π_i(x)

    I think it works fine
    """
    pi = 0
    for row in BGSblock:
        pi += pi_projection(x,row)
    return pi

block = np.array([[ -82, -42,-178,-211,  52,  22, -32,  78,  -9, -51, -63, 279, 200, 280],
 [ 145,   0, -84,  53, 211,-203, 195, -35,  15,  92,  38, -56, 172,-150],
 [ 120,  76,  66, 249, 152,-220, -65, 124,  53, 161,-120, 209,-131, -39]])


B_gs, Mym = gram_schmidt(block)
print(np.linalg.norm(PI(block[1],B_gs))**2)


for i in range(3):
    print(np.linalg.norm(block[i])**2)


print(221223*4/3)