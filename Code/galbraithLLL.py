from utils.utilFunctions import *


def size_reduction(k, Bm,B_gs,Mym):
    for j in reversed(range(0,k)):
        qj = np.round(Mym[k,j])
        Bm[k,:] = Bm[k,:] - qj*Bm[j,:]
        # print(Bm)
        B_gs, Mym = gram_schmidt(Bm)
    return Bm,B_gs, Mym


def remove_dependency(k, Bm):
    Bm = np.delete(Bm, k, 0)
    B_gs, Mym = gram_schmidt(Bm)
    B_gs_norm = calc_norm(B_gs)
    return Bm, B_gs, Mym, B_gs_norm

def Galbraith_LLL_removing_linear_dependence(Bm,delta = 3/4, norm_cutoff = 0.001):
    """
    Beware that close vectors might be removed, so they can't be TOO close 
    """
    n = Bm.shape[0]  #number of rows
    B_gs, Mym = gram_schmidt(Bm)
    print("B_gs:")
    print(np.round(B_gs))
    # print(Mym)
    B_gs_norm = calc_norm(B_gs)
    k = 1
    while k < n:
        # print(k)
        Bm,B_gs,Mym = size_reduction(k, Bm,B_gs,Mym)
        # print(B_gs_norm[k])
        if B_gs_norm[k] < norm_cutoff:    #Must think more here
            """So if very close to 0, in other words seems like linearly dependent"""
            Bm, B_gs, Mym, B_gs_norm = remove_dependency(k,Bm)
            n -= 1
            k = 1
        elif B_gs_norm[k] >= (delta - Mym[k,k-1]**2)*B_gs_norm[k-1]:
            k = k + 1
        else:
            Bm[[k, k-1],:] = Bm[[k-1, k],:]
            B_gs, Mym = gram_schmidt(Bm)
            B_gs_norm = calc_norm(B_gs)
            k = max(1,k-1)
    return Bm




def angle_between_vectors_in_degrees(vector1, vector2):
    """
    Just ChatGpt on this one cause lazy
    """
    dot_product = np.dot(vector1, vector2)
    magnitude1 = np.linalg.norm(vector1)
    magnitude2 = np.linalg.norm(vector2)
    
    cosine_angle = dot_product / (magnitude1 * magnitude2)
    angle_in_radians = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    angle_in_degrees = np.degrees(angle_in_radians)
    
    return angle_in_degrees

if __name__ == "__main__":
    # Bm = np.array([[13, 22, 32, 14], 
    #                [43, 54, 53, 153], 
    #                [43, 51, 6, 1],
    #                [46, 431, 6, 14],
    #                [43, 51, 6, 1]])
    Bm = np.array([
    [ -7,  0, -1,-17,-38, 11, 27],
    [  2, -9,-20, 25, 24, 35, -5],
    [ 11, 51, 13,-24, 27,  7, 15],
    [ 29,  5, -3, 33,-37,-36, -5],
    [ 53,  0,-24, -5, 10, 19,-29],
    [  8,-39,-63,  4, 18,-21, 13],
    [ 47,-22, 52,-12, 43, 22, 10],
    [ -8, 39, 63, -4,-18, 21,-13]])
    print("B:")
    print(Bm)
    # print(gram_schmidt(Bm)[0])
    # print()
    Bm = Galbraith_LLL_removing_linear_dependence(Bm)
    print("Svar\n", Bm)
    # for i in range(len(Bm)):
    #     for j in range(len(Bm)):
    #         print(angle_between_vectors_in_degrees(Bm[i],Bm[j]))




