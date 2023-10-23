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


def update_block(Bm, b_, j, k, delta):
    """
    Updates the block Bm with the new shortest vector b_
    """
    #Now we have a new shorter vector
    #Insert into block 
    block = Bm[:k,:]
    block = np.insert(block, j, b_, 0)     #IS it really position j?????
    block = Galbraith_LLL_removing_linear_dependence(block, delta)
    Bm[:k,:] = block
    B_gs, Mym = gram_schmidt(Bm)
    return Bm, B_gs, Mym


def shortest_vector_and_prints(Bm,tempblock, j, k, bound, B_gs, Mym):
    a, b_ = enum_short_vector(tempblock,bound)
    return b_


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
        b_ = shortest_vector_and_prints(Bm,tempblock, j, k, bound, B_gs, Mym)


        """
        Then the actual code starts
        """
        if (b_ == Bm[j]).all() or (b_ == -Bm[j]).all():
            z += 1
        elif delta * np.linalg.norm(PI(b_, B_gs[j:k,:])) < np.linalg.norm(B_gs[j]):
            Bm, B_gs, Mym = update_block(Bm, b_, j, k, delta)
            z = 0
        else:
            z += 1
            Bm = Galbraith_LLL_removing_linear_dependence(Bm, 0.99)
        j += 1


    return Bm




if __name__ == "__main__":
    Bm = np.random.randint(100, size=(8, 8)) 
#     Bm = np.array([[44,58,38,36,84,97,76],
#  [31,16,45,35,33,55,66],
#  [19, 4,96,72,26,58,11],
#  [78,72,56,61,61,15,49],
#  [47,76,79, 3,74,16,59],
#  [ 9,12,46,98,10,35,85],
#  [29,25,65,10, 9,20,71]])
    # Bm = np.array([[1,0,0],[0,1,0],[0,0,1]])
    # Bm = np.array([[33,89,18,17,30],
#  [ 3,42,93,48,26],
#  [17, 4,67,63,74],
#  [55,36,77,92,17],
#  [34,36,70, 9,84]])
    print("Bm")
    print(np.array2string(Bm,separator=','))
    BKZBm = BKZ(Bm, 3/4, beta = 3)
    print()
    print("BKZBm")
    print(np.array2string(BKZBm,separator=','))

    B_gs, Mym = gram_schmidt(BKZBm)
    for i in range(8):
        print(np.linalg.norm(PI(BKZBm[i], B_gs[i:7,:])))



# print(np.linalg.norm(np.array([ 14 ,-38, -26,  15,  48])))
# print(np.linalg.norm(np.array([ 52 ,-6, -16,  44,  -9])))