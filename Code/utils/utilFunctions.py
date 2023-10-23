import numpy as np
import time as t

def make_square_matrix(Bm):
    r, k = Bm.shape
    if r == k:
        return Bm
    dim = max(r,k)
    newBm = np.zeros((dim,dim))
    newBm[:r,:k] = Bm
    return newBm



def calc_norm(B_gs):
    B_gs_norm = []
    for rownr in range(B_gs.shape[0]):
        B_gs_norm.append(np.linalg.norm(B_gs[rownr,:])**2)
    return B_gs_norm

def gram_schmidt(Bm):
    """
    Computes my own QR thing. 

    Removes all 0 rows. Seems to work well

    Gives so Mym@B_gs is Bm.
    ------------------------------------
    Mym: (r,r)
    B_gs: (r,k)
    """
    Bm = Bm[~np.all(Bm == 0, axis=1)]  #Removing all zero rows
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




if __name__ == "__main__":
    # c = np.array(
    #     [[  9,  -8,   8,  -4],
    #     [  2,  15,  12,   9],
    #     [ -7 , -6  ,10 , 16],
    #     [ 14 ,  2, -18 , 10]])
    # a , b= gram_schmidt(c)


    # for i in range(4):
    #     print(np.linalg.norm(a[i]))
    #     # print(np.linalg.norm(c[i]))
    # print(a)
    # print(b)
    Bm = np.array(
        [[  9,  -8,   8,  -4],
        [  0,  0,  0,   9],
        [  0,  0,  0,   3],
        [  0,  0,  0,   9],
        [  2,  15,  12,   9],
        [  2,  15,  12,   9]])
    print("B:")
    print(Bm)
    Bstar,Mym = gram_schmidt(Bm)
    print()
    print("B*:")
    print(Bstar)
    print()
    print("Mym:")
    print(Mym)
    print("Back")
    print(Mym@Bstar)



















# b_gs,my = gram_schmidt(Bm)
# print(b_gs)
# print(my)

# for row in range(b_gs.shape[0]):
#     print(np.linalg.norm(b_gs[row,:])**2)
#     print(np.inner(b_gs[row,:],b_gs[row,:]))



# def L3FP_removing_linear_dependence(Bm,delta):

#     def swap():  #Can this be global inside this function??
#         if B_gs_norm[k] < (delta - Mym[k,k-1]**2)*B_gs_norm[k-1]:
#             Bm[[k, k-1],:] = Bm[[k-1, k],:]
#             B_gs[[k, k-1],:] = B_gs[[k-1, k],:]
#             B_gs_norm[k-1,k] = B_gs_norm[k-1,k,-1]  #Switch places
#             k = max(1,k-1)
#         else:
#             k = k+1

#     def size_reduct():
#         if abs(Mym[k,j]) > 1/2:
#             qj = np.round(Mym[k,j])
#             if abs(qj) > 2**(tau/2):
#                 Fc = True 
#             for i in range(j):
#                 Mym[k,i] = Mym[k,i] - qj*Mym[j,i]
#             Mym[k,j] = Mym[k,j] - qj

                
                
#             Bm[k,:] = Bm[k,:] - qj*Bm[j,:]
#             # B_gs, Mym = gram_schmidt(Bm)



#     n = len(Bm)  #Is this the correct one??
#     B_gs, Mym = gram_schmidt(Bm)
#     B_gs_norm = []
#     for row in range(len(B_gs)):
#         bi = B_gs[row,:]
#         B_gs_norm.append(np.inner(bi,bi))

#     k = 1
#     while k < n:
#         for j in reversed(range(0,k)):
#             qj = np.round(Mym[k,j])
#             Bm[k,:] = Bm[k,:] - qj*Bm[j,:]
#             B_gs, Mym = gram_schmidt(Bm)

#         swap()


    
            

#     return Bm
 

