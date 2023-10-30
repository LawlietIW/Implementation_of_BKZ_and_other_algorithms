import numpy as np
from betterUtils import *
import time as time

def sub_RED(k,l, Bm, Mym):
    if abs(Mym[k,l]) <= 0.5:
        return Bm, Mym   #Probably not needed
    
    q = np.floor(0.5 + Mym[k,l])   #round to nearest integer
    Bm[k] = Bm[k] - q*Bm[l]
    Mym[k,l] = Mym[k,l] - q
    for i in range(l):
        Mym[k,i] = Mym[k,i] - q*Mym[l,i]
    return Bm,  Mym 


# def step2(k, Bm, B_gs, Mym, B_norms, epsilon = 0.05):
#     """Incremental Gram-Schmidt"""
#     for j in range(k):
#         if B_norms[j] > epsilon:
#             Mym[k,j] = np.inner(Bm[k],B_gs[j])/B_norms[j]
#         else:
#             Mym[k,j] = 0
#     print("Thing in sum:", [Mym[k,j]*B_gs[j] for j in range(k)])
#     B_gs[k] = Bm[k] - sum([Mym[k,j]*B_gs[j] for j in range(k)])
#     B_norms[k] = np.linalg.norm(B_gs[k])**2
#     return B_gs, Mym, B_norms



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
        # print("Before:" , B_norms)
        B_norms[[k-1,k]] = B_norms[[k,k-1]]
        # print("After:", B_norms)
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
    # print("k:", k)
    # print("kmax:", kmax)
    # print("Bm in 3: ")
    # print(Bm)
    # print("Mym in 3: ")
    # print(Mym)

    if B_norms[k] < (delta - Mym[k,k-1]**2) * B_norms[k-1]:
        # print("Swap")
        Bm, Mym, B_norms = swapG(k, kmax, Bm, Mym, B_norms)
        # print("Bm after swap: ")
        # print(Bm)
        # print("Mym after swap: ")
        # print(Mym)
        k = max(1,k-1)
        k, Bm, Mym, B_norms = step3(k, kmax, Bm, Mym, B_norms, delta)
    else:
        # print("Reduce")
        for l in reversed(range(0,k-1)):
            Bm, Mym = sub_RED(k,l, Bm, Mym)
        k += 1
        # print("Bm after reduce: ")
        # print(Bm)
        # print("Mym after reduce: ")
        # print(Mym)
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
            # print()
            # print()
            # print("Step 2")
            # print("Bm before: ")
            # print(Bm)
            # print("B_gs before: ")
            # print(B_gs)
            # print("Mym before: ")
            # print(Mym)
            kmax = k
            B_gs, Mym = gram_schmidt(Bm)
            B_norms = calc_norm(B_gs)
        # print("B_gs after:")
        # print(B_gs)
        # print("Mym after:")
        # print(Mym)
        """Step 3"""
        # print()
        # print()
        # print("Step 3")
        # B_gs[[k-1,k]] = B_gs[[k, k-1]]
        k, Bm, Mym, B_norms = step3(k, kmax, Bm, Mym, B_norms, delta)
        
    return Bm
            

if __name__ == "__main__":
    # Bm = np.random.randint(100, size=(20, 20))
    Bm = np.array([[381, 372, 479, 114, 178, 393, 348, 131, 229, 313, 260, 225, 304, 428,
  134,  70, 458, 156,  48, 158, 154, 472, 448,  98,  89, 458,  74, 404,
  129, 202],
 [330,  67, 110,  82, 187, 183, 113, 341, 224,  53, 372,  74, 361, 456,
  308, 342, 134,  59, 410, 324, 141, 279, 450, 224, 158, 453, 281, 276,
   97, 484],
 [485, 374, 381, 287, 415, 362, 252, 305, 282, 365, 143, 432, 470, 117,
  364,  29, 293,  79, 317,  28, 227,  51, 192, 120, 185, 303, 453,  14,
  366, 485],
 [365, 335,  33, 431,  22, 368,  80, 425, 446, 104, 498, 477, 329, 295,
  435, 203, 379,  30,  18, 374, 470, 266, 305, 329,  96, 361, 339, 378,
   18, 416],
 [ 10, 419, 201, 128, 177, 202, 263, 355, 310,  76, 206,  49, 314, 105,
   68, 207,   3, 184, 476,  29, 333, 420, 239, 432,  85, 260, 250, 295,
  292, 304],
 [424, 432, 406, 164, 124, 102, 125, 461, 340, 326, 275, 343, 150, 404,
  357, 207, 177, 107, 116, 287, 197,  36,  92,  40, 204,  13, 138, 306,
  176, 493],
 [ 67, 225,  43, 233, 320, 436, 215, 248, 154, 145, 118, 407, 387, 414,
  305, 425, 387, 368,  95,  24, 271, 141,  65, 351, 440, 172, 423, 192,
   35, 333],
 [318, 460, 190,  65, 448,  49, 449, 225, 355, 149,  79,  82,  11, 330,
  130, 246, 222, 122, 202, 163,   5, 129, 278, 316, 253, 445,  47, 459,
    0, 276],
 [342, 148,  72, 238, 359, 262, 309,  80,  88, 499,   0,  48, 228,  56,
  265,  40, 388, 178, 321, 321, 496, 499, 275, 318,  56, 227, 321, 218,
  238, 237],
 [177,  29, 153, 300,  42, 289, 395, 288, 184, 331, 297, 252,  21, 136,
  394,  30, 356, 162, 387, 319, 126,   8, 235,  74, 101, 245, 211, 492,
  122,  30],
 [195, 171, 353,  33, 261, 256, 114, 170, 395, 119, 492, 498, 471, 224,
  146, 277, 326, 128, 339, 360,  15, 288,  47, 484, 320, 494, 146, 423,
   55, 239],
 [373, 300,  32, 224,  52,  15,  71, 260, 316, 117,  92,  30, 286, 302,
   87, 162, 262,  57, 412, 204,  10, 465, 274, 411, 401,   7, 447, 412,
  249, 160],
 [454, 144,   2, 332, 131, 130, 173, 480, 222, 239, 453, 449, 396, 175,
   27, 159, 249, 450, 220, 231, 279, 481, 282, 372, 368,  27,  34, 422,
  435,  98],
 [ 22,  33, 223,  68, 412,  44, 140, 316, 150, 288, 186,  40, 368, 466,
  405, 387, 294, 436, 407,  79, 198, 479, 290, 306, 420,  17, 490, 210,
  456, 125],
 [236, 435, 107, 238, 332, 221, 436, 412, 394, 316, 427, 200, 406, 359,
  446, 199, 145, 434, 410, 186, 380, 239, 226, 144, 347, 244, 317, 343,
  179, 499],
 [ 30, 178, 423, 151, 439, 487,  66, 204, 479,  77, 144, 459, 425, 287,
  113, 237, 352, 466, 183,  22, 423, 388, 154, 175, 190, 397, 420,  99,
  494, 187],
 [340, 274, 429, 105, 456, 234, 173, 421,  99, 348, 255, 486, 353, 224,
  293, 274, 291,  16, 212, 344, 447, 300, 162, 132, 454, 348, 204,  58,
  211, 427],
 [302,  32, 228, 413, 344, 252, 210, 120, 431, 368, 134, 371,  48, 377,
  211, 152, 167,  93, 145, 173, 116, 448, 442, 485, 402, 224, 364, 101,
  229, 298],
 [190,  72, 256,  61, 477, 433, 236, 327, 284, 165, 298, 170, 326, 156,
  397, 301, 242, 196,  75, 207, 356,  11, 367,  66, 148, 234, 278,  75,
  287, 259],
 [358, 322, 190,  61, 299, 484, 435, 297, 428,  34, 419, 232, 496, 273,
  196, 320, 424, 120, 114, 438, 140,  92,   2, 484, 439, 457, 353, 197,
   22, 253],
 [468, 254, 139, 424, 109, 348, 194, 278, 275, 255, 368, 240, 204, 129,
  190, 474, 171, 282, 481, 332, 212, 485, 177, 401, 391, 374, 382, 299,
  288, 477],
 [173, 115, 473, 310, 459, 282,  16, 226, 278,  10, 375, 421, 141, 318,
  274, 152,  81, 198,  74, 314,  21, 446, 443, 411, 354, 346,   2, 291,
  222, 480],
 [ 84, 434, 270, 485, 401, 377, 281, 180, 193, 458, 351, 330, 426, 283,
   96, 137, 474, 306, 255, 493, 340, 227, 381, 332, 483, 280,  85,  36,
  466, 186],
 [451, 363, 484,  99, 426,  34, 258, 212, 115, 437, 106,   2,  32, 353,
  496, 418, 386, 358, 155, 235, 268, 405, 321,  80,  67, 287, 451, 462,
  271, 388],
 [244, 451, 209,  94, 176, 118, 153, 133, 347,  21, 189, 467, 458, 456,
  423, 123,  43,  21, 296, 121, 443, 147, 321, 149, 112, 346,  39, 295,
  136, 360],
 [151, 287,  39, 339, 246, 144,  64, 359, 134, 318,  21, 357, 139, 440,
  242, 181, 215, 381,  62, 230, 287, 109, 444, 450, 222, 442,  35, 260,
  433, 114],
 [226, 377,  18, 273, 162, 383, 471, 290, 314, 263, 276, 450,  86, 277,
  138,  70, 296,  45, 136, 248, 135, 356, 174, 134, 264, 496, 350, 295,
  157, 454],
 [ 98, 264,  59,  11, 321, 132, 219,  60, 312, 212, 334, 320,  37, 323,
  158, 395, 467, 345, 104, 289, 263, 390, 446, 208, 338, 254, 331, 192,
  116, 236],
 [146, 216,   5, 365, 138, 157, 205, 266, 329, 182,  17, 302,  66, 199,
  104, 133, 139,  70, 326, 329, 149, 497, 275, 321, 499, 130,  74, 220,
  133, 158],
 [337,   9, 186,  88,  90, 240,  49, 272, 113, 420, 427, 287, 115, 403,
  186, 119, 198, 273, 176, 252, 235, 442, 109, 100, 474, 210, 127, 348,
  238,  79]])
#     Bm = np.array([[20, 16, 23, 91, 98, 11, 94, 68,  3],
#  [48, 63, 28,  2,  1, 31, 96, 92,  2],
#  [16, 29,  5, 38, 48, 75, 16, 47, 88],
#  [34, 95, 98, 19,  2, 13, 24, 78, 32],
#  [65, 23,  6, 34, 87, 28, 74, 33, 24],
#  [93, 26, 78, 22, 19, 43, 10, 48, 58],
#  [74, 33, 84, 78, 13, 65, 71, 12, 32],
#  [51, 62, 74, 93, 91, 14, 89, 43, 97],
#  [90,  7, 58, 31, 68, 28, 28, 29, 38]])
#     Bm = np.array([[34, 61, 20],
#  [72, 91, 15],
#  [22, 83, 47]])
    # print("Bm: ")
    # print(np.array2string(Bm, separator=', '))
    start = time.time()
    LLL = main_LLL(Bm)
    print("Time taken:", time.time() - start)
    # print("LLL:")
    # print(LLL)



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
