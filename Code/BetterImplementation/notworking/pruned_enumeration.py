import numpy as np
from BetterImplementation.sameUtilsasinfirstimplementation import *


def find_lattice_vectors(Bm, B_gs, Mym, B_norms, R_squared):
    r,c = Bm.shape
    sigma = np.zeros((r+1,r))
    r_vec = np.linspace(0,r,r+1)
    # print(r_vec)
    rho = np.zeros(r+1)
    v = np.zeros(r)
    v[0] = 1
    c = np.zeros(r)
    w = np.zeros(r)
    last_nonzero = 1
    k = 0   #Try this

    while True:
        rho[k] = rho[k + 1] + (v[k] - c[k])**2 * B_norms[k]
        print("rho:", rho)
        print("R_squared:", R_squared[r-1-k])
        if rho[k] <= (R_squared[r-1-k]):
            if k == 0:
                return v
            else:
                k -= 1
                r_vec[k] = max(r_vec[k], r_vec[k + 1])
                for i in reversed(range(k+1,int(r_vec[k+1]))):
                    sigma[i][k] = sigma[i + 1][k] + v[i] * Mym[i,k]
                c[k] = -sigma[k + 1,k]
                v[k] = round(c[k])
                w[k] = 1
        else:
            k += 1
            if k == r:
                return None
            r_vec[k-1] = k
            print("r_vec:", r_vec)
            if k >= last_nonzero:
                last_nonzero = k
                v[k] += 1
            else:
                if v[k] > c[k]:
                    v[k] -= w[k]
                else:
                    v[k] += w[k]
                w[k] += 1

# Example usage
if __name__ == "__main__":
    Bm = np.array([[1,0,3],[5,1,17],[6,2,20]])
    r,c = Bm.shape
    B_gs, Mym = gram_schmidt(Bm)
    B_norms = calc_norm(B_gs)
    # print(B_norms)
    R = 1
    R_squared = [(i/(r))*R**2 for i in range(1,r+1)]
    print("R_squared:", R_squared)
    result = find_lattice_vectors(Bm, B_gs, Mym, B_norms, R_squared)
    if result is not None:
        print("Lattice vectors satisfying the bounds:", result)
    else:
        print("No solution exists.")
