from utils.utilFunctions import *


def enumeration(Bm, B_gs, Mym, epsilon=1e-10):
    """
    Based on https://www.ush.it/team/ascii/CRC.Algorithmic.Cryptanalysis.Jun.2009.eBook-ELOHiM.pdf, Algorithm 10.6

    It doesn't work because alpha is not floored of all, so it becomes decimal which is obviously wrong. If I change it everything is wrong suddenly
    """
    r, k = Bm.shape    #For row and kolumn
    B_gs_norm = calc_norm(B_gs)
    print("r: ", r)
    alpha_best = np.zeros(r)
    alpha_best[0] = 1

    print("alpha_best: ", alpha_best)
    L_best = np.linalg.norm(Bm[0,:])**2
    print("L_best: ", L_best)

    alpha = np.zeros(r + 1)
    alpha[r] = 0 

    print("norm: ", B_gs_norm[-1])
    alpha[r - 1] = - np.floor(np.sqrt( L_best/B_gs_norm[r-1]) + epsilon)
    print("alpha: ", alpha)

    L_tilde = np.zeros(r+1)
    L_tilde[r] = 0
    print("L_tilde: ", L_tilde)
    print()
    t = r - 1

    while t <= r - 1:
        if t == -1:
            cvec = np.dot(alpha[:r], Bm)
            L = np.linalg.norm(cvec)**2
            print(L)
            print(ejrhqlkjerh)
            if L < L_best:
                L_best = L
                alpha_best = alpha.copy()

            alpha[0] += 1
            t = 0
        else:
            # print(alpha[t + 1:r-1])
            # print(Mym[t + 1:r-1,t])
            beta = alpha[t] + np.dot(alpha[t + 1:r], Mym[t + 1:r,t])
            print("beta: ", beta)
            L_tilde[t] = L_tilde[t + 1] + (beta**2) * B_gs_norm[t]
            print("L_tilde: ", L_tilde)
            if L_tilde[t] < L_best + epsilon:
                if t > 0:
                    print(Mym[t:r,t-1])
                    print(alpha[t:r])
                    beta = np.dot(alpha[t:r], Mym[t:r,t-1])
                    print("beta: ", beta)
                    print("Shit: ", np.floor(np.sqrt( (L_best - L_tilde[t])/B_gs_norm[t-1]) + epsilon))
                    alpha[t - 1] = - np.floor(np.sqrt((L_best - L_tilde[t])/B_gs_norm[t-1]) + epsilon - beta)
                    print("alpha: ", alpha)
                    print()
                    # print(frbqkjfew)
                t -= 1
            else:
                alpha[t + 1] += 1
                t += 1

    return alpha_best   

# Example usage
Bm = np.array([[201,37,35],[148,297,53],[24,532,12]])
B_gs, Mym = gram_schmidt(Bm)

print("B:")
print(Bm)
B_gs,Mym = gram_schmidt(Bm)
print()
print("B*:")
print(B_gs)
print()
print("Mym:")
print(Mym)
print()

shortest_vector = enumeration(Bm,B_gs, Mym)
print("Shortest vector in the basis B:")
print(shortest_vector)




