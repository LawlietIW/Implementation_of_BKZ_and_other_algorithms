from utils.utilFunctions import *
import numpy as np
import time


def calc_M1(i,a,A_squared,n,Mym,B_gs_norm):
    """
    Calculates M1 as described in my paper

    ---------------
    Just KG with notation by Galbraith
    """
    outer_sum = 0
    for j in range(i + 1,n):
        inner_sum = np.dot(a[j + 1:], Mym[j + 1:, j])
        outer_sum += (a[j] + inner_sum)**2 * B_gs_norm[j]
    return np.sqrt((A_squared - outer_sum)/B_gs_norm[i])

def calc_M2(i,a,n,Mym):
    """
    Calculates M2 as described in my paper
    """
    return sum([Mym[j,i] * a[j] for j in range(i + 1,n)])  


def recursionpart(i,a,A_squared,Bm, Mym, B_gs_norm):
    """Implementation of the method described in GalBraith"""
    r = Bm.shape[0]
    if i == -1:
        #Now we have found all a's downwards. Let's see if we have something apart from the 0 vector
        new_shortest_vector = np.dot(a,Bm)
        
        #So Avect is now the shortest current vector
        A_squared = np.inner(new_shortest_vector,new_shortest_vector) - 1  #Just to make sure we find something a bit smaller next
        return (A_squared,a)
        
    M1 = calc_M1(i,a,A_squared,r,Mym,B_gs_norm)
    M2 = calc_M2(i,a,r,Mym)
    lowlim = np.ceil(- M1 - M2)
    highlim = np.floor(M1 - M2)
    possiblea = np.arange(lowlim,highlim + 1,1) #Just to also get the top
    if possiblea.size == 0:
        return
    acopy = np.copy(a)
    for aes in possiblea:
        acopy[i] = aes
        Alpha = recursionpart(i-1,acopy,A_squared,Bm,Mym,B_gs_norm)
        if Alpha:  #So if we get anything, then we return all the way up
            return Alpha
            
        
def loop_until_not_zero_vector(r,a,A_squared,Bm,Mym,B_gs_norm):
    """
    The function that keeps updating A_squared until we find the shortest one not 0
    """
    while True:
        A_squared, newa = recursionpart(r-1,a,A_squared,Bm, Mym, B_gs_norm) 
        if A_squared == -1: #If only the zero vector was shorter, we have our best_a
            break
        else:
            best_a = newa
    return best_a


def enum_short_vector(Bm,A_squared):
    """
    Currently only working for r <= k.
    """
    r = Bm.shape[0]   #Number of rows
    B_gs,Mym = gram_schmidt(Bm)
    B_gs_norm = [np.inner(B_gs[i,:],B_gs[i,:]) for i in range(r)]
    a = np.zeros(r)

    best_a = loop_until_not_zero_vector(r,a,A_squared,Bm,Mym,B_gs_norm)

    shortest_vector = sum([best_a[l]*Bm[l,:] for l in range(r)])
    return best_a, shortest_vector


if __name__ == "__main__":
    Bm = np.random.randint(500, size=(20,20))
    # Bm = np.array([[1,0,3],[5,1,17],[6,2,20]])
    print(np.array2string(Bm, separator=', '))

    A_squared = np.inner(Bm[0],Bm[0])  #So this is Asquared
    start = time.time()
    a, shortestVect = enum_short_vector(Bm,A_squared) 
    print("Time taken:", time.time() - start)

    # print("Shortest Vector:", shortestVect, "\na: ", a)