from utils.utilFunctions import *
from galbrathLLL2 import Galbraith_LLL_removing_linear_dependence
from myOldEnumeration import enum_short_vector

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

# def vector_projection(vector, matrix_of_row_vectors):
#     A = np.array(matrix_of_row_vectors)
#     projection_matrix = np.dot(A, np.linalg.inv(np.dot(A.T, A)))
#     projection = np.dot(projection_matrix, vector)
#     return projection


def BKZ(Bm, delta, beta):
    """
    Description
    """
    r,k = Bm.shape

    z = 0
    j = 0         #So we start at 0
    Bm = Galbraith_LLL_removing_linear_dependence(Bm, delta)
    B_gs, Mym = gram_schmidt(Bm)
    # print(B_gs)
    # print()
    # print(PI(B_gs[1], 0, 1, B_gs))
    while z < r - 1:
        j = (j % (r - 1))              #So we start at 0
        k = min(j + beta, r)
        tempblock = Bm[j:k,:]
        bound = np.inner(tempblock[0],tempblock[0])
        print()
        print("Bm after LLL")
        print(Bm)
        print()
        print("Block we find shortest vector in:")
        print(tempblock)
        print()
        a, b_ = enum_short_vector(tempblock,bound)
        print()
        print()
        print(np. around(B_gs[j:k,:], 2))
        print("shortest vector in this one is: ", b_)
        print("left:", np.linalg.norm(PI(b_, B_gs[j:k,:])))
        # print("chat", vector_projection(b_, B_gs[j:k,:]))
        print("right",   np.linalg.norm(B_gs[j]))
        print()
        if np.linalg.norm(PI(b_, B_gs[j:k,:])) < np.linalg.norm(B_gs[j]):
            #Now we have a new shorter vector
            #Insert into block 
            block = Bm[:k,:]
            block = np.insert(block, j, b_, 0)     #IS it really position j?????
            print("Block after insertion")
            print(np.array2string(block,separator = ','))
            block = Galbraith_LLL_removing_linear_dependence(block, delta)
            print("Block after LLL")
            print(block)
            Bm[:k,:] = block
            B_gs, Mym = gram_schmidt(Bm)
            # print(ewkfjakjef)
        else:
            z += 1
            Bm = Galbraith_LLL_removing_linear_dependence(Bm, 0.99)

        j += 1


    return Bm




if __name__ == "__main__":
    Bm = np.random.randint(100, size=(5, 5)) 
#     Bm = np.array([[44,58,38,36,84,97,76],
#  [31,16,45,35,33,55,66],
#  [19, 4,96,72,26,58,11],
#  [78,72,56,61,61,15,49],
#  [47,76,79, 3,74,16,59],
#  [ 9,12,46,98,10,35,85],
#  [29,25,65,10, 9,20,71]])
    # Bm = np.array([[1,0,0],[0,1,0],[0,0,1]])
    print(Bm)
    print()
    print(np.array2string(Bm,separator=','))
    BKZBm = BKZ(Bm, 3/4, beta = 3)
    # print("Bm")
    print("BKZBm")
    print(np.array2string(BKZBm,separator=','))

    B_gs, Mym = gram_schmidt(BKZBm)
    # for i in range(7):
    #     print(np.linalg.norm(PI(BKZBm[i], i, 7, B_gs)))

