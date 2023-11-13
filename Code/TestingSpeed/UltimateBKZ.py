from BKZ_first_implementation.utils.utilFunctions import *  #I use this one, doesn't matter which util, they are identical

def update_block(Bm, b_, j, k, delta, LLL):
    """
    Updates the block Bm with the new shortest vector b_
    """
    #Now we have a new shorter vector
    #Insert into block 
    block = Bm[:k]
    block = np.insert(block, j, b_, 0)     #IS it really position j?????
    block = LLL(block, delta)
    Bm[:k] = block
    return Bm


def shortest_vector_and_prints(tempblock, ENUM):
    tempB_gs, tempMym = gram_schmidt(tempblock)
    tempB_norms = calc_norm(tempB_gs)
    a, b_, c_bar = ENUM(tempblock, tempMym, tempB_norms)
    return b_, c_bar, tempB_norms[0]


def ultimate_BKZ(Bm, LLL, ENUM, delta = 0.75, beta = 5):
    """
    Description
    """
    r,k = Bm.shape

    z = 0
    j = 0         #So we start at 0
    Bm = LLL(Bm, delta)
    while z < r - 1:
        j = (j % (r - 1))              #So we start at 0
        k = min(j + beta, r)
        tempblock = Bm[j:k,:]
        b_, c_bar, B_gs_norm_first_in_block = shortest_vector_and_prints(tempblock, ENUM)


        """
        Then the actual code starts
        """
        if (b_ == Bm[j]).all() or (b_ == -Bm[j]).all(): #If the shortest is already first
            z += 1
        elif delta * B_gs_norm_first_in_block >  c_bar:
            Bm_updated = update_block(Bm, b_, j, k, delta, LLL)
            if Bm_updated.all() == Bm.all(): #If nothing changed
                z += 1
            else:
                Bm = Bm_updated
                z = 0
        else:
            z += 1
            Bm = LLL(Bm, 0.99)
        j += 1


    return Bm